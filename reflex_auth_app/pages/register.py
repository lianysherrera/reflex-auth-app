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
                                disabled=AuthState.is_loading,
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
                                disabled=AuthState.is_loading,
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Contraseña", size="2", weight="medium"),
                            rx.hstack(
                                rx.input(
                                    name="password",
                                    type=rx.cond(AuthState.show_password, "text", "password"),
                                    placeholder="Mínimo 8 caracteres",
                                    width="100%",
                                    disabled=AuthState.is_loading,
                                ),
                                rx.icon_button(
                                    rx.cond(
                                        AuthState.show_password,
                                        rx.icon("eye-off", size=18),
                                        rx.icon("eye", size=18),
                                    ),
                                    on_click=AuthState.toggle_show_password,
                                    variant="ghost",
                                    size="2",
                                    disabled=AuthState.is_loading,
                                ),
                                width="100%",
                                align="center",
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        rx.vstack(
                            rx.text("Confirmar contraseña", size="2", weight="medium"),
                            rx.hstack(
                                rx.input(
                                    name="confirm_password",
                                    type=rx.cond(AuthState.show_confirm_password, "text", "password"),
                                    placeholder="Repite tu contraseña",
                                    width="100%",
                                    disabled=AuthState.is_loading,
                                ),
                                rx.icon_button(
                                    rx.cond(
                                        AuthState.show_confirm_password,
                                        rx.icon("eye-off", size=18),
                                        rx.icon("eye", size=18),
                                    ),
                                    on_click=AuthState.toggle_show_confirm_password,
                                    variant="ghost",
                                    size="2",
                                    disabled=AuthState.is_loading,
                                ),
                                width="100%",
                                align="center",
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
                            loading=AuthState.is_loading,
                            variant="ghost",
                            color="white",
                            border="1px solid white",
                            background="transparent",
                            _hover={"color": "#c0c0c0", "border": "1px solid #c0c0c0", "background": "transparent"},
                            transition="color 0.2s, border-color 0.2s",
                            margin_top="0.75em",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=AuthState.handle_register,
                    reset_on_submit=True,
                    width="100%",
                ),
                rx.hstack(
                    rx.text("¿Ya tienes cuenta?", size="2", color="gray"),
                    rx.link(
                        "Iniciar sesión",
                        href="/login",
                        size="2",
                        color="white",
                        _hover={"color": "#c0c0c0"},
                        transition="color 0.2s",
                    ),
                    spacing="1",
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