import reflex as rx

from reflex_auth_app.components.avatar import user_avatar
from reflex_auth_app.state.auth_state import AuthState


def navbar() -> rx.Component:
    return rx.hstack(
        rx.link(
            rx.heading("Reflex Auth App", size="5"),
            href="/",
        ),
        rx.spacer(),
        rx.cond(
            AuthState.is_logged_in,
            rx.dropdown_menu.root(
                rx.dropdown_menu.trigger(
                    rx.hstack(
                        user_avatar(),
                        rx.text(
                            AuthState.current_user_name,
                            size="2",
                            weight="medium",
                        ),
                        rx.icon("chevron-down", size=16),
                        align="center",
                        spacing="2",
                        cursor="pointer",
                    ),
                ),
                rx.dropdown_menu.content(
                    rx.dropdown_menu.item(
                        rx.hstack(
                            rx.icon("user", size=16),
                            rx.text("Ver perfil"),
                            spacing="2",
                            align="center",
                        ),
                        on_click=rx.redirect("/profile"),
                    ),
                    rx.dropdown_menu.separator(),
                    rx.dropdown_menu.item(
                        rx.hstack(
                            rx.icon("log-out", size=16),
                            rx.text("Cerrar sesión"),
                            spacing="2",
                            align="center",
                        ),
                        on_click=AuthState.handle_logout,
                        color="red",
                    ),
                ),
            ),
            rx.hstack(
                rx.link("Iniciar sesión", href="/login"),
                rx.link("Registrarse", href="/register"),
                spacing="4",
                align="center",
            ),
        ),
        width="100%",
        padding="1em 2em",
        align="center",
        border_bottom="1px solid var(--gray-5)",
    )
