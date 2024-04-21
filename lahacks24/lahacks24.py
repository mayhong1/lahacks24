import json
import reflex as rx
from rxconfig import config
from vibe_generator import username_to_eras_playlist
from typing import List, Dict

# The app state
class State(rx.State):
    image_url = ""
    username = ""
    playlist_processing = False
    playlist_loaded = False

    # Stores the playlist data for each era
    data1: List[Dict[str, List[Dict[str, str]]]] = {}
    data2: List[Dict[str, List[Dict[str, str]]]] = {}
    data3: List[Dict[str, List[Dict[str, str]]]] = {}
    
    # Runs when "make playlist" button is pressed
    def generate_playlist(self, form_data: dict):

        # Get username
        self.form_data = form_data
        self.username = form_data['prompt_text']

        # Start loading icon
        self.playlist_loaded = False
        self.playlist_processing = True
        yield
        

        print(form_data['prompt_text'])

        # Generate playlist data into song_list[0-2].txt
        username_to_eras_playlist(self.username)

        print("*** FINISHED PROCESSING ***\n")

        # No more loading icon
        self.playlist_processing = False
        self.playlist_loaded = True

        # Load playlist data into data[1-3]
        with open("song_list0.txt", 'r') as file:
            self.data1 = json.load(file)
        with open("song_list1.txt", 'r') as file:
            self.data2 = json.load(file)
        with open("song_list2.txt", 'r') as file:
            self.data3 = json.load(file)

        # Redirect to the eras page
        return rx.redirect("/eras_page")

# Homepage
@rx.page(route="/")
def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("make a playlist out of your vibe", font_size="1.5em"),
            rx.text("we analyze your instagram feed, detect the vibe, and make a playlist out of your vibe."),

            # Form to enter username
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
            rx.cond(
                State.playlist_processing,
                rx.chakra.circular_progress(is_indeterminate=True),
            ),
            width="25em",
            bg="white",
            padding="2em",
            align="center",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle, rgba(174,208,238,1) 0%, rgba(233,148,213,1) 100%)",
    )

# Playlists page
@rx.page(route="/eras_page")
def eras_page() -> rx.Component:
    return rx.box(
        rx.box(
            rx.heading(f"{State.username}'s eras tour", size="7", align="center", style=dict(paddingBottom="2%", paddingTop="2%", color="white")),
            rx.text("using AI, we analyzed your instagram feed, discovered these eras of your life, and made playlists based off the vibe.", color="white", align="center", style=dict(paddingBottom="2%", paddingTop="0%")),
            background="rgba(18, 11, 38, 0.8)"
        ),
        rx.grid(
            rx.box(
                rx.heading(f"{State.data1[0]['vibe']} era", size="5", align="center", style=dict(paddingBottom="3%", paddingTop="2%", maxWidth="70%", margin="0 auto")),
                rx.image(
                    src= f"/{State.username}-era1[0].jpg",
                    width="200px",
                    height="auto",
                    box_shadow="lg",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),
                rx.text(f"during this time of your life, you were {State.data1[0]['words'][0]}, {State.data1[0]['words'][1]}, {State.data1[0]['words'][2]}, {State.data1[0]['words'][3]}, {State.data1[0]['words'][4]}, {State.data1[0]['words'][5]}, {State.data1[0]['words'][6]}, and {State.data1[0]['words'][7]}", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text(f"{State.data1[0]['songs'][0]['title']} - {State.data1[0]['songs'][0]['artist']}", align="center"),
                    rx.text(f"{State.data1[0]['songs'][1]['title']} - {State.data1[0]['songs'][1]['artist']}", align="center"),
                    rx.text(f"{State.data1[0]['songs'][2]['title']} - {State.data1[0]['songs'][2]['artist']}", align="center"),
                    rx.text(f"{State.data1[0]['songs'][3]['title']} - {State.data1[0]['songs'][3]['artist']}", align="center"),
                    rx.text(f"{State.data1[0]['songs'][4]['title']} - {State.data1[0]['songs'][4]['artist']}", align="center"),
                ),
            ),
            rx.box(
                rx.heading(f"{State.data2[0]['vibe']} era", size="5", align="center", style=dict(paddingBottom="3%", paddingTop="2%", maxWidth="70%", margin="0 auto")),
                rx.image(
                    src= f"/{State.username}-era2[0].jpg",
                    width="200px",
                    height="auto",
                    box_shadow="5g",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),
                rx.text(f"you seem {State.data2[0]['words'][0]}, {State.data2[0]['words'][1]}, {State.data2[0]['words'][2]}, {State.data2[0]['words'][3]}, {State.data2[0]['words'][4]}, {State.data2[0]['words'][5]}, {State.data2[0]['words'][6]}, and {State.data2[0]['words'][7]} during this era", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text(f"{State.data2[0]['songs'][0]['title']} - {State.data2[0]['songs'][0]['artist']}", align="center"),
                    rx.text(f"{State.data2[0]['songs'][1]['title']} - {State.data2[0]['songs'][1]['artist']}", align="center"),
                    rx.text(f"{State.data2[0]['songs'][2]['title']} - {State.data2[0]['songs'][2]['artist']}", align="center"),
                    rx.text(f"{State.data2[0]['songs'][3]['title']} - {State.data2[0]['songs'][3]['artist']}", align="center"),
                    rx.text(f"{State.data2[0]['songs'][4]['title']} - {State.data2[0]['songs'][4]['artist']}", align="center"),
                ),
            ),
            rx.box(
                rx.heading(f"{State.data3[0]['vibe']} era", size="5", align="center", style=dict(paddingBottom="3%", paddingTop="2%", maxWidth="70%", margin="0 auto")),
                rx.image(
                    src= f"/{State.username}-era3[0].jpg",
                    width="200px",
                    height="auto",
                    box_shadow="lg",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),

                    rx.text(f"you're giving {State.data3[0]['words'][0]}, {State.data3[0]['words'][1]}, {State.data3[0]['words'][2]}, {State.data3[0]['words'][3]}, {State.data3[0]['words'][4]}, {State.data3[0]['words'][5]}, {State.data3[0]['words'][6]}, and {State.data3[0]['words'][7]}", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                    rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text(f"{State.data3[0]['songs'][0]['title']} - {State.data3[0]['songs'][0]['artist']}", align="center"),
                    rx.text(f"{State.data3[0]['songs'][1]['title']} - {State.data3[0]['songs'][1]['artist']}", align="center"),
                    rx.text(f"{State.data3[0]['songs'][2]['title']} - {State.data3[0]['songs'][2]['artist']}", align="center"),
                    rx.text(f"{State.data3[0]['songs'][3]['title']} - {State.data3[0]['songs'][3]['artist']}", align="center"),
                    rx.text(f"{State.data3[0]['songs'][4]['title']} - {State.data3[0]['songs'][4]['artist']}", align="center"),
                ),
            ),
            columns="3",
            rows="1",
            width="100%",
            height="100%",
        ),
        rx.center(
            rx.button(
                "generate on spotify",
                type="submit",
                size="3",
                marginTop="4%",
                marginBottom="4%",
                background="rgba(18, 11, 38, 0.8)"
            )
        ),
        height="100%",
        background="radial-gradient(circle, rgba(205,227,246,1) 1%, rgba(211,210,241,1) 25%, rgba(218,198,239,1) 45%, rgba(204,189,232,1) 61%, rgba(228,182,233,1) 80%, rgba(233,148,213,1) 100%)",
    )

# Initialize website
app = rx.App()
app.add_page(index)
app.add_page(eras_page)