import reflex as rx
from reflex_auth_app.pages.register import register_page
from reflex_auth_app.pages.login import login_page
from reflex_auth_app.pages.dashboard import dashboard_page

from reflex_auth_app.utils.db import init_db


def index() -> rx.Component:
    return rx.box(
        rx.color_mode.button(position="top-right"),
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
                rx.link(
                    rx.button(
                        "Registrarse",
                        size="3",
                        variant="solid",
                        cursor="pointer",
                    ),
                    href="/register",
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
app.add_page(register_page, route="/register")
app.add_page(login_page, route="/login")
app.add_page(dashboard_page, route="/dashboard")