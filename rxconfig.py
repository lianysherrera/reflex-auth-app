import reflex as rx

config = rx.Config(
    app_name="reflex_auth_app",
    db_url="sqlite:///auth.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)