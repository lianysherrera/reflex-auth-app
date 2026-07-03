import reflex as rx

from reflex_auth_app.state.auth_state import AuthState
from reflex_auth_app.components.navbar import navbar


def login_page() -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.center(
            rx.vstack(
                rx.vstack(
                    rx.heading("Inicia sesión", size="7"),
                    rx.text(
                        "Ingresa tus datos para acceder a tu cuenta.",
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
                            rx.text("Email", size="2", weight="medium"),
                            rx.input(
                                name="email",
                                type="email",
                                placeholder="tu@email.com",
                                width="100%",
                                disabled=AuthState.is_loading,
                                on_change=lambda _: AuthState.reset_login_error(),
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
                                    placeholder="Tu contraseña",
                                    width="100%",
                                    disabled=AuthState.is_loading,
                                    on_change=lambda _: AuthState.reset_login_error(),
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
                        rx.cond(
                            AuthState.login_error != "",
                            rx.callout(
                                AuthState.login_error,
                                color_scheme="red",
                                size="1",
                                width="100%",
                            ),
                        ),
                        rx.button(
                            "Iniciar sesión",
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
                    on_submit=AuthState.handle_login,
                    reset_on_submit=True,
                    width="100%",
                ),
                rx.text(
                    "¿No tienes cuenta? ",
                    rx.link("Regístrate", href="/register"),
                    size="2",
                    color="gray",
                    margin_top="1em",
                ),
                spacing="4",
                width="100%",
                max_width="360px",
                padding="2em",
            ),
            height="100vh",
        ),
    )
