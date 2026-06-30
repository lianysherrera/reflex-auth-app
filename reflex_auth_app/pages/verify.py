import reflex as rx

from reflex_auth_app.components.navbar import navbar
from reflex_auth_app.state.auth_state import AuthState


def verify_page() -> rx.Component:
    # Página que procesa el link de verificación de email.
    return rx.fragment(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading("Verificación de cuenta", size="7"),
                rx.cond(
                    AuthState.verify_success,
                    rx.callout(
                        AuthState.verify_message,
                        color_scheme="green",
                        size="2",
                    ),
                    rx.callout(
                        AuthState.verify_message,
                        color_scheme="red",
                        size="2",
                    ),
                ),
                rx.link("Ir a iniciar sesión", href="/login"),
                spacing="4",
                align="center",
                padding="2em",
            ),
            height="100vh",
        ),
    )
