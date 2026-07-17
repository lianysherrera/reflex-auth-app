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
                rx.hstack(
                    user_avatar(size="72px"),
                    rx.vstack(
                        rx.hstack(
                            rx.heading(AuthState.current_user_name, size="6"),
                            rx.link(
                                rx.icon("layout-dashboard", size=18),
                                href="/dashboard",
                                color="gray",
                                title="Ir al dashboard",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(AuthState.current_user_email, color="gray", size="2"),
                        rx.cond(
                            AuthState.current_user_bio != "",
                            rx.text(AuthState.current_user_bio, color="gray", size="2"),
                        ),
                        spacing="1",
                        align="start",
                    ),
                    spacing="4",
                    align="center",
                    padding_bottom="0.5em",
                ),
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
                # Formulario de perfil (nombre + bio)
                rx.form(
                    rx.vstack(
                        rx.text(
                            "Nombre",
                            size="2",
                            weight="medium",
                            color="gray",
                        ),
                        rx.input(
                            name="name",
                            default_value=AuthState.current_user_name,
                            placeholder="Tu nombre",
                            background="transparent",
                            border="1px solid white",
                            width="100%",
                        ),
                        rx.divider(),
                        rx.text(
                            "Bio",
                            size="2",
                            weight="medium",
                            color="gray",
                        ),
                        rx.text_area(
                            name="bio",
                            default_value=AuthState.current_user_bio,
                            placeholder="Escribe algo sobre ti...",
                            background="transparent",
                            border="1px solid white",
                            width="100%",
                            rows="3",
                        ),
                        rx.button(
                            rx.icon("save", size=16),
                            rx.text("Guardar"),
                            type="submit",
                            size="2",
                            variant="outline",
                            background="transparent",
                            border="1px solid white",
                            color="white",
                            cursor="pointer",
                            style={
                                "_hover": {
                                    "background": "rgba(255, 255, 255, 0.15)",
                                },
                            },
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=AuthState.handle_update_profile,
                    width="100%",
                ),
                rx.divider(),
                # Mensajes de éxito/error de contraseña
                rx.cond(
                    AuthState.password_error != "",
                    rx.callout(
                        AuthState.password_error,
                        color_scheme="red",
                        size="1",
                        width="100%",
                    ),
                ),
                rx.cond(
                    AuthState.password_success != "",
                    rx.callout(
                        AuthState.password_success,
                        color_scheme="green",
                        size="1",
                        width="100%",
                    ),
                ),
                # Formulario de cambio de contraseña
                rx.form(
                    rx.vstack(
                        rx.text(
                            "Cambiar contraseña",
                            size="3",
                            weight="bold",
                        ),
                        rx.text(
                            "Contraseña actual",
                            size="2",
                            weight="medium",
                            color="gray",
                        ),
                        rx.hstack(
                            rx.input(
                                name="current_password",
                                type=rx.cond(AuthState.show_current_password, "text", "password"),
                                placeholder="Tu contraseña actual",
                                background="transparent",
                                border="1px solid white",
                                width="100%",
                            ),
                            rx.icon_button(
                                rx.cond(
                                    AuthState.show_current_password,
                                    rx.icon("eye-off", size=18),
                                    rx.icon("eye", size=18),
                                ),
                                on_click=AuthState.toggle_show_current_password,
                                variant="ghost",
                                size="2",
                                type="button",
                            ),
                            width="100%",
                            align="center",
                        ),
                        rx.text(
                            "Nueva contraseña",
                            size="2",
                            weight="medium",
                            color="gray",
                        ),
                        rx.hstack(
                            rx.input(
                                name="new_password",
                                type=rx.cond(AuthState.show_new_password, "text", "password"),
                                placeholder="Mínimo 8 caracteres",
                                background="transparent",
                                border="1px solid white",
                                width="100%",
                            ),
                            rx.icon_button(
                                rx.cond(
                                    AuthState.show_new_password,
                                    rx.icon("eye-off", size=18),
                                    rx.icon("eye", size=18),
                                ),
                                on_click=AuthState.toggle_show_new_password,
                                variant="ghost",
                                size="2",
                                type="button",
                            ),
                            width="100%",
                            align="center",
                        ),
                        rx.text(
                            "Confirmar nueva contraseña",
                            size="2",
                            weight="medium",
                            color="gray",
                        ),
                        rx.hstack(
                            rx.input(
                                name="confirm_new_password",
                                type=rx.cond(AuthState.show_confirm_new_password, "text", "password"),
                                placeholder="Repite la nueva contraseña",
                                background="transparent",
                                border="1px solid white",
                                width="100%",
                            ),
                            rx.icon_button(
                                rx.cond(
                                    AuthState.show_confirm_new_password,
                                    rx.icon("eye-off", size=18),
                                    rx.icon("eye", size=18),
                                ),
                                on_click=AuthState.toggle_show_confirm_new_password,
                                variant="ghost",
                                size="2",
                                type="button",
                            ),
                            width="100%",
                            align="center",
                        ),
                        rx.button(
                            rx.icon("key-round", size=16),
                            rx.text("Actualizar contraseña"),
                            type="submit",
                            size="2",
                            variant="outline",
                            background="transparent",
                            border="1px solid white",
                            color="white",
                            cursor="pointer",
                            style={
                                "_hover": {
                                    "background": "rgba(255, 255, 255, 0.15)",
                                },
                            },
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=AuthState.handle_change_password,
                    reset_on_submit=True,
                    width="100%",
                ),
                spacing="5",
                width="100%",
                max_width="480px",
                padding="2em",
            ),
        ),
    )