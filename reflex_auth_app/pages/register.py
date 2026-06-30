import reflex as rx

from reflex_auth_app.state.auth_state import AuthState
from reflex_auth_app.components.navbar import navbar


def register_page() -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.heading("Crea tu cuenta", size="7"),
                    rx.text(
                        "Regístrate con tu email para empezar.",
                        color="gray",
                        size="2",
                    ),
                    spacing="1",
                    align="center",
                    margin_bottom="1.5em",
                ),
                rx.form(
                    rx.vstack(
                        rx.vstack(
                            rx.text("Nombre", size="2", weight="medium"),
                            rx.input(
                                name="name",
                                placeholder="Tu nombre o alias",
                                width="100%",
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Email", size="2", weight="medium"),
                            rx.input(
                                name="email",
                                type="email",
                                placeholder="tu@email.com",
                                width="100%",
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Contraseña", size="2", weight="medium"),
                            rx.input(
                                name="password",
                                type="password",
                                placeholder="Mínimo 8 caracteres",
                                width="100%",
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Confirmar contraseña", size="2", weight="medium"),
                            rx.input(
                                name="confirm_password",
                                type="password",
                                placeholder="Repite tu contraseña",
                                width="100%",
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        rx.cond(
                            AuthState.register_error != "",
                            rx.callout(
                                AuthState.register_error,
                                color_scheme="red",
                                size="1",
                                width="100%",
                            ),
                        ),
                        rx.cond(
                            AuthState.register_success != "",
                            rx.callout(
                                AuthState.register_success,
                                color_scheme="green",
                                size="1",
                                width="100%",
                            ),
                        ),
                        rx.button(
                            "Crear cuenta",
                            type="submit",
                            width="100%",
                            size="3",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=AuthState.handle_register,
                    reset_on_submit=True,
                    width="100%",
                ),
                rx.hstack(
                    rx.text("¿Ya tienes cuenta?", size="2"),
                    rx.link("Iniciar sesión", href="/login", size="2"),
                    spacing="2",
                    justify="center",
                ),
                spacing="4",
                width="100%",
                max_width="360px",
                padding="2em",
            ),
            height="100vh",
        ),
    )