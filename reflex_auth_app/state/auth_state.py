import asyncio
import re
from typing import Optional

import reflex as rx
import sqlmodel

import uuid
from reflex_auth_app.utils.email import send_verification_email

from reflex_auth_app.models import Session, User
from reflex_auth_app.utils import hash_password, verify_password

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MIN_PASSWORD_LENGTH = 8
SESSION_COOKIE_NAME = "session_token"


class AuthState(rx.State):

    register_error: str = ""
    register_success: str = ""
    login_error: str = ""
    session_token: str = rx.Cookie("", name=SESSION_COOKIE_NAME)

    @rx.var
    def is_logged_in(self) -> bool:
        return self._get_current_user() is not None

    @rx.var
    def current_user_name(self) -> str:
        user = self._get_current_user()
        if user is None:
            return ""
        return user.name


    def require_login(self):
        if not self.is_logged_in:
            return rx.redirect("/login")

    def reset_register_messages(self):
        self.register_error = ""
        self.register_success = ""

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

        name = form_data.get("name", "").strip()
        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            self.register_error = "Por favor completa todos los campos."
            return

        if not EMAIL_REGEX.match(email):
            self.register_error = "El formato del email no es válido."
            return

        if len(password) < MIN_PASSWORD_LENGTH:
            self.register_error = (
                f"La contraseña debe tener al menos {MIN_PASSWORD_LENGTH} caracteres."
            )
            return

        if password != confirm_password:
            self.register_error = "Las contraseñas no coinciden."
            return

        with rx.session() as session:
            existing_user = session.exec(
                sqlmodel.select(User).where(User.email == email)
            ).first()

            if existing_user is not None:
                self.register_error = "Ya existe una cuenta registrada con ese email."
                return

            verification_token = uuid.uuid4().hex

            new_user = User(
                name=name,
                email=email,
                password_hash=hash_password(password),
                verification_token=verification_token,
            )
            session.add(new_user)
            session.commit()

        send_verification_email(email, verification_token)

        self.register_success = "¡Cuenta creada! Revisa tu email para verificar tu cuenta antes de iniciar sesión."
        yield
        await asyncio.sleep(3)
        self.register_success = ""

    # Mensaje a mostrar en la página de verificación.
    verify_message: str = ""
    verify_success: bool = False

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

    def handle_login(self, form_data: dict):
        self.login_error = ""

        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "")

        if not email or not password:
            self.login_error = "Por favor completa todos los campos."
            return

        with rx.session() as session:
            user = session.exec(
                sqlmodel.select(User).where(User.email == email)
            ).first()

            if user is None or not verify_password(password, user.password_hash):
                self.login_error = "Email o contraseña incorrectos."
                return

            if not user.is_verified:
                self.login_error = "Debes verificar tu email antes de iniciar sesión. Revisa tu bandeja de entrada."
                return

            new_session = Session(user_id=user.id)
            session.add(new_session)
            session.commit()
            session.refresh(new_session)

            self.session_token = new_session.token

        return rx.redirect("/dashboard")

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