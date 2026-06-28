import reflex as rx

from reflex_auth_app.state.auth_state import AuthState


def dashboard_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.cond(
                AuthState.is_logged_in,
                rx.vstack(
                    rx.heading("¡Hola ", AuthState.current_user_name, "!", size="7"),
                    rx.button(
                        "Cerrar sesión",
                        on_click=AuthState.handle_logout,
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.vstack(
                    rx.text("No has iniciado sesión.", color="gray"),
                    rx.link("Iniciar sesión", href="/login"),
                    spacing="3",
                    align="center",
                ),
            ),
            spacing="4",
            align="center",
        ),
        height="100vh",
    )