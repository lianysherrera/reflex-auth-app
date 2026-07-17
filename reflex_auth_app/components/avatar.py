import reflex as rx

from reflex_auth_app.components.boring_avatar import boring_avatar
from reflex_auth_app.state.auth_state import AuthState

def user_avatar(size: str = "36px") -> rx.Component:
    return boring_avatar(
        name=AuthState.current_user_email,
        variant="beam",
        size=size,
    )