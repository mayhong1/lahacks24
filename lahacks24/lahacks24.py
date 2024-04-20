"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config
from vibe_generator import username_to_playlist

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""
    def generate_playlist(self, form_data: dict):
        self.form_data = form_data
        print(form_data['prompt_text'])
        username_to_playlist(form_data['prompt_text'])



def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("make a playlist out of your vibe", font_size="1.5em"),
            rx.text("we analyze your instagram feed, detect the vibe, and make a playlist out of your vibe."),
            rx.form(
                rx.vstack(
                    rx.input(
                        id="prompt_text",
                        placeholder="enter instagram username..",
                        size="3",
                    ),
                    rx.button(
                        "make playlist",
                        type="submit",
                        size="3",
                    ),
                    align="stretch",
                    spacing="2",
                ),
                width="100%",
                on_submit=State.generate_playlist,
            ),
            rx.divider(),
            width="25em",
            bg="white",
            padding="2em",
            align="center",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )


app = rx.App()
app.add_page(index)
