import reflex as rx
from reflex_auth_app.pages.register import register_page
from reflex_auth_app.pages.login import login_page
from reflex_auth_app.pages.dashboard import dashboard_page
from reflex_auth_app.pages.verify import verify_page
from reflex_auth_app.state.auth_state import AuthState
from reflex_auth_app.utils.db import init_db
from reflex_auth_app.components.navbar import navbar


def index() -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading(
                    "Sistema de autenticación con Reflex",
                    size="9",
                    text_align="center",
                    weight="bold",
                ),
                rx.text(
                    "Gestiona tus usuarios de forma segura y sencilla.",
                    size="4",
                    color_scheme="gray",
                    text_align="center",
                ),
                spacing="6",
                align="center",
            ),
            min_height="100vh",
        ),
    )


init_db()

app = rx.App()
app.add_page(index)
app.add_page(register_page, route="/register", on_load=[AuthState.redirect_if_logged_in, AuthState.reset_register_messages])
app.add_page(login_page, route="/login", on_load=[AuthState.redirect_if_logged_in, AuthState.reset_login_error])
app.add_page(dashboard_page, route="/dashboard", on_load=AuthState.require_login)
app.add_page(verify_page, route="/verify", on_load=AuthState.handle_verify)