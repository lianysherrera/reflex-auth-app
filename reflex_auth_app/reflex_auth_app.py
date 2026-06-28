import reflex as rx
from rxconfig import config
from reflex_auth_app.pages.register import register_page

from reflex_auth_app.utils.db import init_db


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


init_db()

app = rx.App()
app.add_page(index)
app.add_page(register_page, route="/register")