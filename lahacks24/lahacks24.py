"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""

@rx.page(route="/")
def index() -> rx.Component:
    return rx.center(
        rx.theme_panel(),
        rx.vstack(
<<<<<<< Updated upstream
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text("Get started by editing ", rx.code(filename)),
            rx.button(
                "Check out our docs!",
                on_click=lambda: rx.redirect(docs_url),
                size="4",
=======
            rx.heading("make a playlist out of your vibe", font_size="1.5em", align="center"),
            rx.text("we analyze your instagram feed, detect the vibe, and make a playlist out of your vibe.", align="center"),
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
>>>>>>> Stashed changes
            ),
            rx.logo(),
            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )

@rx.page(route="/eras_page")
def eras_page() -> rx.Component:
    return rx.box(
        rx.heading("username's eras tour", size="7", align="center", style=dict(paddingBottom="2%", paddingTop="3%")),
        rx.text("using AI, we analyzed your instagram feed, discovered these eras of your life, and made a playlist based off the vibe.", align="center", style=dict(paddingBottom="2%", paddingTop="0%")),
        rx.grid(
            rx.box(
                rx.heading("study era", size="5", align="center", style=dict(paddingBottom="3%", paddingTop="2%")),
                rx.image(
                    src="/testimage.jpg",
                    width="200px",
                    height="auto",
                    box_shadow="lg",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),
                rx.text(
                    rx.text.em("september 2023"),
                    style=dict(paddingBottom="2%", maxWidth="70%", margin="0 auto"), 
                    align="center"
                ),
                rx.text("in this era you grinded out work at the library or a cafe while look effortlessly cool doing so", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text("ivy - frank ocean", align="center"),
                    rx.text("sunflower - post malone", align="center"),
                    rx.text("style - taylor swift", align="center"),
                    rx.text("maniac - conan gray", align="center"),
                    rx.text("last friday night - katy perry", align="center"),
                ),
            ),
            rx.box(
                rx.heading("main character era", size="5", align="center", style=dict(paddingBottom="3%", paddingTop="2%")),
                rx.image(
                    src="/5.jpg",
                    width="200px",
                    height="auto",
                    box_shadow="5g",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),
                rx.text(
                    rx.text.em("november 2017"),
                    style=dict(paddingBottom="2%", maxWidth="70%", margin="0 auto"), 
                    align="center"
                ),
                rx.text("in this era you were a main character sunt in culpa qui officia deserunt mollit anim id ", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text("sicko mode - travis scott", align="center"),
                    rx.text("heather - conan gray", align="center"),
                    rx.text("mr. rager - kid cudi", align="center"),
                    rx.text("the last great american dynasty - taylor swift", align="center"),
                    rx.text("kilby girl - the backseat lovers", align="center"),
                ),
            ),
            rx.box(
                rx.heading("indie boy era", size="5", align="center", style=dict(paddingBottom="3%", paddingTop="2%")),
                rx.image(
                    src="/4.jpg",
                    width="200px",
                    height="auto",
                    box_shadow="lg",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),
                rx.text(
                    rx.text.em("july 2019"),
                    style=dict(paddingBottom="2%", maxWidth="70%", margin="0 auto"), 
                    align="center"
                ),
                rx.text("in this era you were an indie boy aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                    rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text("kyoto - phoebe bridgers", align="center"),
                    rx.text("trouble - cage the elephant", align="center"),
                    rx.text("lemon boy - cavetown", align="center"),
                    rx.text("roddy - djo", align="center"),
                    rx.text("hot rod - day glow", align="center"),
                ),
            ),
            bg="white",
            background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
            columns="3",
            rows="1",
            width="100%",
            height="100%",
        ),
        background="white",

    )

'''
def Card(title, description, link=None):
  """Reusable card component with title, description, and optional avatar and link."""
  return rx.card(
      rx.link(
          rx.flex(
              rx.icon("music-2"),
              rx.box(
                  rx.heading(title),
                  rx.text(description),
              ),
              spacing="2",
          ),
          href=None,  # Set href attribute if link provided
      ),
      as_child=True,
  )
'''

app = rx.App()
app.add_page(index)
app.add_page(eras_page)