import asyncio
import re
from typing import Optional

import reflex as rx
import sqlmodel


from reflex_auth_app.models import Session, User
from reflex_auth_app.utils import hash_password, verify_password, generate_avatar_color

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

    @rx.var
    def is_logged_in(self) -> bool:
        return self._get_current_user() is not None

    @rx.var
    def current_user_name(self) -> str:
        user = self._get_current_user()
        if user is None:
            return ""
        return user.name

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
                        new_user = User(
                            name=name,
                            email=email,
                            password_hash=hash_password(password),
                            avatar_color=generate_avatar_color(),
                        )
                        session.add(new_user)
                        session.commit()
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

        self.register_success = "¡Cuenta creada! Ya puedes iniciar sesión."
        yield
        await asyncio.sleep(3)
        self.register_success = ""

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