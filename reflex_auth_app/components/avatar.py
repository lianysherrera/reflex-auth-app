import reflex as rx

from reflex_auth_app.state.auth_state import AuthState

def user_avatar(size: str = "36px", font_size: str = "14px") -> rx.Component:
    return rx.box(
        rx.text(
            AuthState.user_initials,
            color="white",
            font_weight="bold",
            font_size=font_size,
        ),
        width=size,
        height=size,
        border_radius="50%",
        background_color=AuthState.avatar_color,
        display="flex",
        align_items="center",
        justify_content="center",
        flex_shrink="0",
    )