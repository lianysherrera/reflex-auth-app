import reflex as rx

from reflex_auth_app.components.navbar import navbar
from reflex_auth_app.state.auth_state import AuthState


def note_card(note) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(note["title"], size="3", weight="bold", flex="1"),
                rx.icon_button(
                    rx.icon("trash-2", size=14),
                    on_click=AuthState.delete_note(note["id"]),
                    variant="ghost",
                    color_scheme="red",
                    size="1",
                    cursor="pointer",
                ),
                align="start",
                width="100%",
            ),
            rx.cond(
                note["content"] != "",
                rx.text(
                    note["content"],
                    size="2",
                    color_scheme="gray",
                    style={"white_space": "pre-wrap", "word_break": "break-word"},
                ),
            ),
            rx.text(note["created_at"], size="1", color_scheme="gray"),
            spacing="2",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def new_note_form() -> rx.Component:
    return rx.card(
        rx.form(
            rx.vstack(
                rx.heading("Nueva nota", size="4", weight="bold"),
                rx.input(
                    placeholder="Título",
                    name="title",
                    required=True,
                    width="100%",
                ),
                rx.text_area(
                    placeholder="Contenido (opcional)",
                    name="content",
                    width="100%",
                    rows="4",
                ),
                rx.cond(
                    AuthState.note_error != "",
                    rx.callout(
                        AuthState.note_error,
                        color_scheme="red",
                        size="1",
                        width="100%",
                    ),
                ),
                rx.button(
                    "Guardar nota",
                    type="submit",
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            on_submit=AuthState.create_note,
            reset_on_submit=True,
        ),
        width="100%",
    )


def dashboard_page() -> rx.Component:
    return rx.fragment(
        navbar(),
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            "Mis notas",
                            size="7",
                            weight="bold",
                        ),
                        rx.text(
                            rx.cond(
                                AuthState.notes_count == 0,
                                "Aún no tienes notas. ¡Crea una!",
                                rx.cond(
                                    AuthState.notes_count == 1,
                                    "1 nota guardada",
                                    AuthState.notes_count.to_string() + " notas guardadas",
                                ),
                            ),
                            size="3",
                            color_scheme="gray",
                        ),
                        spacing="1",
                        align="start",
                    ),
                    justify="between",
                    width="100%",
                ),
                rx.divider(),
                new_note_form(),
                rx.cond(
                    AuthState.notes_count > 0,
                    rx.vstack(
                        rx.heading("Tus notas", size="4", weight="medium"),
                        rx.vstack(
                            rx.foreach(AuthState.notes, note_card),
                            spacing="3",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),
                spacing="5",
                width="100%",
                max_width="640px",
                align="start",
            ),
            padding="2em",
            min_height="100vh",
            display="flex",
            justify_content="center",
        ),
    )