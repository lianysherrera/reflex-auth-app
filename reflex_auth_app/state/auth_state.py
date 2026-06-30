import asyncio
import re
from typing import Optional

import reflex as rx
import sqlmodel

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

            new_user = User(
                name=name,
                email=email,
                password_hash=hash_password(password),
            )
            session.add(new_user)
            session.commit()

        self.register_success = "¡Cuenta creada exitosamente! Ya puedes iniciar sesión."
        yield
        await asyncio.sleep(3)
        self.register_success = ""

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