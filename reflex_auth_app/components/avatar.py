import reflex as rx

from reflex_auth_app.state.auth_state import AuthState

def user_avatar() -> rx.Component:
    return rx.box(
        rx.text(
            AuthState.user_initials,
            color="white",
            font_weight="bold",
            font_size="14px",
        ),
        width="36px",
        height="36px",
        border_radius="50%",
        background_color=AuthState.avatar_color,
        display="flex",
        align_items="center",
        justify_content="center",
    )