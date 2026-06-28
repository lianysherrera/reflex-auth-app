import re

import reflex as rx
import sqlmodel

from reflex_auth_app.models import User
from reflex_auth_app.utils import hash_password

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

MIN_PASSWORD_LENGTH = 8


class AuthState(rx.State):
    register_error: str = ""
    register_success: str = ""

    def handle_register(self, form_data: dict) -> None:
        self.register_error = ""
        self.register_success = ""

        email = form_data.get("email", "").strip().lower()
        password = form_data.get("password", "")
        confirm_password = form_data.get("confirm_password", "")

        # Validaciones

        if not email or not password or not confirm_password:
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

        # Verificar que el email no esté ya registrado

        with rx.session() as session:
            existing_user = session.exec(
                sqlmodel.select(User).where(User.email == email)
            ).first()

            if existing_user is not None:
                self.register_error = "Ya existe una cuenta registrada con ese email."
                return

            # Crear usuario con la contraseña hasheada

            new_user = User(
                email=email,
                password_hash=hash_password(password),
            )
            session.add(new_user)
            session.commit()

        self.register_success = "¡Cuenta creada exitosamente! Ya puedes iniciar sesión."