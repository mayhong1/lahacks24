"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
import reflex as rx
from vibe_generator import username_to_eras_playlist
from typing import Optional
from reflex import page, box, heading


docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"
#only one class State otherwise conflicts in state mngmnt
class State(rx.State):
    """the app state"""
    hovered: Optional[str] = None
    def handle_mouse_enter(cls, button_name):
        cls.hovered = button_name

    def handle_mouse_leave(cls):
        cls.hovered = None
    def generate_playlist(self, form_data: dict):
        self.form_data = form_data
        print(form_data['prompt_text'])
        username_to_eras_playlist(form_data['prompt_text'])


def handle_mouse_enter(button_name):
    State.hovered = button_name
    return None

def handle_mouse_leave():
     State.hovered = None
     return None 



@rx.page(route="/")
def index() -> rx.Component:
  # Home playlist settings centered at the top
  
  home_playlist_settings = rx.center(rx.hstack(
      rx.button("Home", 
          color_scheme= rx.cond(State.hovered == "Home", "pink", "light-pink"),
          color=rx.color("indigo", 1),
          background_color=rx.color("pink", alpha=300),

          on_mouse_enter=handle_mouse_enter("Home"),
          on_mouse_leave=handle_mouse_leave(),
          size="4",
          borderRadius="39%",
          margin="30px 0"
          
      ), 
      rx.button("Playlist", 
          color_scheme=rx.cond(State.hovered == "Playlist", "pink","light-pink"),
          on_mouse_enter=handle_mouse_enter("Playlist"),
          on_mouse_leave=handle_mouse_leave(),
          background_color=rx.color("pink", alpha=300),
          borderRadius="39%",
          size="4",
          margin="30px 0",
      ),
      rx.button("Log Out", 
          color_scheme=rx.cond(State.hovered == "Log Out", "pink","light-pink"),
          on_mouse_enter=handle_mouse_enter("Log Out"),
          on_mouse_leave=handle_mouse_leave(),
          borderRadius="39%",
          background_color=rx.color("pink", alpha=300),
          size="4",
          margin="30px 0"
      ),
      justify="center",  #Center the buttons horizontally,
      spacing="3",
      width="100%" #need width="100%" twice for this to work 
  ), width="100%")

  # RetroTune rounded box
  reotrune_box = rx.vstack(
      rx.heading("RetroTune", font_size="1.5em"),
      rx.text("Analyze your Insta vibe & craft a playlist to match."),
      rx.form(
          rx.vstack(
              rx.input(
                  id="prompt_text",
                  placeholder="Enter Instagram Username...",
                  size="3",
                  radius="large",
                  style={"color": "black", "background-color": "white", "border": "1px solid #ccc", "outline": "none", "font-weight":"800", "font-size": "100%"}
              ),
              rx.center(
                  rx.button(
                      "make playlist",
                      type="submit",
                      size="3",
                      radius="full",
                      background_color=rx.color("pink", alpha=300),
                      style={"width": "150px"}
                  )
              ),
              align="stretch",
              spacing="2",
          ),
          width="100%",
          on_submit=State.generate_playlist,
      ),
      rx.divider(),
      bg="white",
      padding="2em",
      align="center",
      borderRadius="10%",
      width="100%"
  )

  # Stack the elements vertically with home settings on top
  return rx.container(rx.vstack(
      home_playlist_settings,
      reotrune_box,
      width="100%",
      height="100vh",
      spacing="9",
      
  ),
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
        size="1",
  )




@rx.page(route="/eras_page")
def eras_page() -> rx.Component:
    return rx.box(
        rx.heading("username's eras tour", size="7", align="center", style=dict(paddingBottom="2%", paddingTop="3%")),
        rx.text("Your Life, Your Music: Our AI has scanned your Instagram to craft playlists that echo the eras of your life.", align="center", style=dict(paddingBottom="2%", paddingTop="0%")),
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


@rx.page(route="log_out")
def log_out() -> rx.Component:
    return Container(
        rx.heading("You have been logged out", size="5", align="center", style={"paddingBottom": "3%", "paddingTop": "2%"}),
        rx.text("Thank you for using RetroTune!", align="center", style={"paddingBottom": "2%"}),
        rx.button(
            "Log In Again",
            on_click=lambda: rx.redirect("/login"),  # Assuming '/login' is your login route
            style={"marginTop": "20px", "display": "block", "margin": "0 auto"}
        ),
        rx.button(
            "Go to Home",
            on_click=lambda: rx.redirect("/"),  # Assuming '/' is your home route
            style={"marginTop": "10px", "display": "block", "margin": "0 auto"}
        ),
        style={"textAlign": "center", "padding": "50px"}
    )

# Additional functions like page_content() should be defined below

app = rx.App()
app.add_page(index)
app.add_page(eras_page)
app.add_page(log_out)
