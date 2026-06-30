import reflex as rx

from reflex_auth_app.state.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.heading("Reflex Auth", size="5"),
                href="/",
            ),
            rx.spacer(),
            rx.cond(
                AuthState.is_logged_in,
                rx.hstack(
                    rx.text(f"Hola, {AuthState.current_user_name}"),
                    rx.button(
                        "Cerrar sesión",
                        on_click=AuthState.handle_logout,
                        variant="soft",
                        cursor="pointer",
                    ),
                    spacing="4",
                    align="center",
                ),
                rx.hstack(
                    rx.link(rx.button("Iniciar sesión", variant="soft"), href="/login"),
                    rx.link(rx.button("Registrarse"), href="/register"),
                    spacing="4",
                    align="center",
                ),
            ),
            width="100%",
            align="center",
            padding="1em",
        ),
        width="100%",
        border_bottom="1px solid var(--gray-5)",
    )
