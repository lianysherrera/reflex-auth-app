import asyncio
import re
import uuid
from typing import Optional

import reflex as rx
import sqlmodel


from reflex_auth_app.models import Session, User
from reflex_auth_app.utils import hash_password, verify_password, generate_avatar_color
from reflex_auth_app.utils.email import send_verification_email

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MIN_PASSWORD_LENGTH = 8
SESSION_COOKIE_NAME = "session_token"


class AuthState(rx.State):

    register_error: str = ""
    register_success: str = ""
    login_error: str = ""
    session_token: str = rx.Cookie("", name=SESSION_COOKIE_NAME)
    show_password: bool = False
    show_confirm_password: bool = False
    is_loading: bool = False
    verify_message: str = ""
    verify_success: bool = False
    profile_error: str = ""
    profile_success: str = ""

    @rx.var
    def is_logged_in(self) -> bool:
        return self._get_current_user() is not None

    @rx.var
    def current_user_name(self) -> str:
        user = self._get_current_user()
        if user is None:
            return ""
        return user.name

    @rx.var
    def user_initials(self) -> str:
        user = self._get_current_user()
        if user is None:
            return ""
        parts = user.name.strip().split()
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    @rx.var
    def avatar_color(self) -> str:
        user = self._get_current_user()
        return user.avatar_color if user is not None else "#4F46E5"

    @rx.var
    def current_user_email(self) -> str:
        user = self._get_current_user()
        if user is None:
            return ""
        return user.email

    @rx.var
    def current_user_bio(self) -> str:
        user = self._get_current_user()
        if user is None or user.bio is None:
            return ""
        return user.bio

    def toggle_show_password(self):
        # Alterna entre mostrar y ocultar el campo de contraseña
        self.show_password = not self.show_password

    def toggle_show_confirm_password(self):
        # Alterna entre mostrar y ocultar e campo de confirmar contraseña
        self.show_confirm_password = not self.show_confirm_password


    def require_login(self):
        if not self.is_logged_in:
            return rx.redirect("/login")

    def redirect_if_logged_in(self):
        if self.is_logged_in:
            return rx.redirect("/dashboard")

    def reset_register_messages(self):
        self.register_error = ""
        self.register_success = ""

    def reset_login_error(self):
        self.login_error = ""

    def _get_current_user(self) -> Optional[User]:
        if not self.session_token:
            return None

        with rx.session() as session:
            db_session = session.exec(
                sqlmodel.select(Session).where(Session.token == self.session_token)
            ).first()

            if db_session is None:
                return None

            return session.exec(
                sqlmodel.select(User).where(User.id == db_session.user_id)
            ).first()

    async def handle_register(self, form_data: dict):
        self.register_error = ""
        self.register_success = ""
        self.is_loading = True
        yield

        error = None
        email_data = None

        try:
            name = form_data.get("name", "").strip()
            email = form_data.get("email", "").strip().lower()
            password = form_data.get("password", "")
            confirm_password = form_data.get("confirm_password", "")

            if not name or not email or not password or not confirm_password:
                error = "Por favor completa todos los campos."
            elif not EMAIL_REGEX.match(email):
                error = "El formato del email no es válido."
            elif len(password) < MIN_PASSWORD_LENGTH:
                error = f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres."
            elif password != confirm_password:
                error = "Las contraseñas no coinciden."
            else:
                with rx.session() as session:
                    existing_user = session.exec(
                        sqlmodel.select(User).where(User.email == email)
                    ).first()

                    if existing_user is not None:
                        error = "Ya existe una cuenta registrada con ese email."
                    else:
                        verification_token = uuid.uuid4().hex
                        new_user = User(
                            name=name,
                            email=email,
                            password_hash=hash_password(password),
                            avatar_color=generate_avatar_color(),
                            verification_token=verification_token,
                        )
                        session.add(new_user)
                        session.commit()
                        email_data = (email, verification_token, name)
        except Exception:
            error = "Error inesperado. Inténtalo de nuevo."
        finally:
            self.is_loading = False

        if error:
            self.register_error = error
            yield
            await asyncio.sleep(6)
            self.register_error = ""
            return

        send_verification_email(*email_data)
        self.register_success = "¡Cuenta creada! Revisa tu email para verificar tu cuenta antes de iniciar sesión."
        yield
        await asyncio.sleep(3)
        self.register_success = ""

    def handle_verify(self):
        token = self.router.page.params.get("token", "")

        if not token:
            self.verify_message = "Link de verificación inválido."
            self.verify_success = False
            return

        with rx.session() as session:
            user = session.exec(
                sqlmodel.select(User).where(User.verification_token == token)
            ).first()

            if user is None:
                self.verify_message = "Este link de verificación no es válido o ya fue usado."
                self.verify_success = False
                return

            user.is_verified = True
            user.verification_token = None
            session.add(user)
            session.commit()

        self.verify_message = "¡Tu cuenta fue verificada exitosamente! Ya puedes iniciar sesión."
        self.verify_success = True

    async def handle_login(self, form_data: dict):
        self.login_error = ""
        self.is_loading = True
        yield

        error = None
        redirect = False

        try:
            email = form_data.get("email", "").strip().lower()
            password = form_data.get("password", "")

            if not email or not password:
                error = "Por favor completa todos los campos."
            else:
                with rx.session() as session:
                    user = session.exec(
                        sqlmodel.select(User).where(User.email == email)
                    ).first()

                    if user is None or not verify_password(password, user.password_hash):
                        error = "Email o contraseña incorrectos."
                    elif not user.is_verified:
                        error = "Debes verificar tu email antes de iniciar sesión. Revisa tu bandeja de entrada."
                    else:
                        new_session = Session(user_id=user.id)
                        session.add(new_session)
                        session.commit()
                        session.refresh(new_session)
                        self.session_token = new_session.token
                        redirect = True
        except Exception:
            error = "Error inesperado. Inténtalo de nuevo."
        finally:
            self.is_loading = False

        if error:
            self.login_error = error
            yield
            await asyncio.sleep(6)
            self.login_error = ""
            return

        if redirect:
            yield rx.redirect("/dashboard")

    def handle_logout(self):
        if self.session_token:
            with rx.session() as session:
                db_session = session.exec(
                    sqlmodel.select(Session).where(
                        Session.token == self.session_token
                    )
                ).first()
                if db_session is not None:
                    session.delete(db_session)
                    session.commit()

        self.session_token = ""
        return rx.redirect("/login")
    
    def handle_update_name(self, form_data: dict) -> None:
        self.profile_error = ""
        self.profile_success = ""

        new_name = form_data.get("name", "").strip()

        if not new_name:
            self.profile_error = "El nombre no puede estar vacío."
            return

        if len(new_name) < 2:
            self.profile_error = "El nombre debe tener al menos 2 caracteres."
            return

        current_user = self._get_current_user()
        if current_user is None:
            self.profile_error = "No se encontró el usuario."
            return

        with rx.session() as session:
            user = session.exec(
                sqlmodel.select(User).where(User.id == current_user.id)
            ).first()

            if user is None:
                self.profile_error = "No se encontró el usuario."
                return

            user.name = new_name
            session.add(user)
            session.commit()

        self.profile_success = "¡Nombre actualizado correctamente!"

    def handle_update_bio(self, form_data: dict) -> None:
        self.profile_error = ""
        self.profile_success = ""

        new_bio = form_data.get("bio", "").strip()

        current_user = self._get_current_user()
        if current_user is None:
            self.profile_error = "No se encontró el usuario."
            return

        with rx.session() as session:
            user = session.exec(
                sqlmodel.select(User).where(User.id == current_user.id)
            ).first()

            if user is None:
                self.profile_error = "No se encontró el usuario."
                return

            user.bio = new_bio if new_bio else None
            session.add(user)
            session.commit()

        self.profile_success = "¡Bio actualizada correctamente!"