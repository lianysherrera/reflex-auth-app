import reflex as rx

from reflex_auth_app.state.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.link(
                rx.heading("Reflex Auth", size="5", color="white", _hover={"color": "#c0c0c0"}, transition="color 0.2s"),
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
                    rx.link(
                        rx.button(
                            "Iniciar sesión",
                            variant="ghost",
                            color="white",
                            border="1px solid white",
                            background="transparent",
                            _hover={"color": "#c0c0c0", "border": "1px solid #c0c0c0", "background": "transparent"},
                            transition="color 0.2s, border-color 0.2s",
                        ),
                        href="/login",
                    ),
                    rx.link(
                        rx.button(
                            "Registrarse",
                            variant="ghost",
                            color="white",
                            border="1px solid white",
                            background="transparent",
                            _hover={"color": "#c0c0c0", "border": "1px solid #c0c0c0", "background": "transparent"},
                            transition="color 0.2s, border-color 0.2s",
                        ),
                        href="/register",
                    ),
                    spacing="6",
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
