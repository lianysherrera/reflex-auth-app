import reflex as rx


class BoringAvatar(rx.Component):
    library = "boring-avatars"
    tag = "Avatar"
    is_default = True

    name: rx.Var[str]
    variant: rx.Var[str] = "beam"
    size: rx.Var[str]
    square: rx.Var[bool] = False


boring_avatar = BoringAvatar.create
