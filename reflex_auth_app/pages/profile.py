import reflex as rx

from reflex_auth_app.components.avatar import user_avatar
from reflex_auth_app.components.navbar import navbar
from reflex_auth_app.state.auth_state import AuthState


def profile_page() -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.center(
            rx.vstack(
                # Cabecera del perfil
                rx.vstack(
                    user_avatar(),
                    rx.heading(AuthState.current_user_name, size="7"),
                    rx.text(AuthState.current_user_email, color="gray", size="2"),
                    spacing="3",
                    align="center",
                    padding_bottom="1em",
                ),
                rx.divider(),
                # Mensajes de éxito/error
                rx.cond(
                    AuthState.profile_error != "",
                    rx.callout(
                        AuthState.profile_error,
                        color_scheme="red",
                        size="1",
                        width="100%",
                    ),
                ),
                rx.cond(
                    AuthState.profile_success != "",
                    rx.callout(
                        AuthState.profile_success,
                        color_scheme="green",
                        size="1",
                        width="100%",
                    ),
                ),
                # Sección 1: Editar nombre 
                rx.vstack(
                    rx.heading("Nombre", size="4"),
                    rx.text(
                        "Así te verán los demás en la aplicación.",
                        color="gray",
                        size="2",
                    ),
                    rx.form(
                        rx.vstack(
                            rx.input(
                                name="name",
                                default_value=AuthState.current_user_name,
                                placeholder="Tu nombre",
                                width="100%",
                            ),
                            rx.button(
                                "Guardar nombre",
                                type="submit",
                                size="2",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        on_submit=AuthState.handle_update_name,
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                    padding="1.5em",
                    border="1px solid var(--gray-5)",
                    border_radius="8px",
                ),
                # Sección 2: Editar bio
                rx.vstack(
                    rx.heading("Bio", size="4"),
                    rx.text(
                        "Cuéntanos algo sobre ti (opcional).",
                        color="gray",
                        size="2",
                    ),
                    rx.form(
                        rx.vstack(
                            rx.text_area(
                                name="bio",
                                default_value=AuthState.current_user_bio,
                                placeholder="Escribe algo sobre ti...",
                                width="100%",
                                rows="4",
                            ),
                            rx.button(
                                "Guardar bio",
                                type="submit",
                                size="2",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        on_submit=AuthState.handle_update_bio,
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                    padding="1.5em",
                    border="1px solid var(--gray-5)",
                    border_radius="8px",
                ),
                spacing="4",
                width="100%",
                max_width="560px",
                padding="2em",
            ),
        ),
    )