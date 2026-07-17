import reflex as rx

from reflex_auth_app.components.navbar import navbar


def not_found_page() -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.center(
            rx.vstack(
                rx.heading(
                    "404",
                    size="9",
                    weight="bold",
                ),
                rx.text(
                    "Esta página no existe.",
                    size="4",
                    color_scheme="gray",
                ),
                rx.link(
                    rx.button(
                        "Volver al inicio",
                        background="transparent",
                        border="1px solid white",
                        color="white",
                    ),
                    href="/",
                ),
                spacing="4",
                align="center",
            ),
            min_height="90vh",
        ),
    )
