"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config
from vibe_generator import username_to_eras_playlist
import json

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"

#loading JSON files

month_dict = {
    1  : "January",
    2  : "Februrary",
    3  : "March",
    4  : "April",
    5  : "May",
    6  : "June",
    7  : "July",
    8  : "August",
    9  : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}

# setting up variables
# title: d

class State(rx.State):
    """The app state."""

    image_url="alicewang10t-era1[0].jpg"
    username=""
    playlist_processing = False
    playlist_loaded = False
    
    def generate_playlist(self, form_data: dict):
        self.form_data = form_data
        self.playlist_loaded = False
        self.playlist_processing = True
        yield
        self.username=form_data['prompt_text']
        print(form_data['prompt_text'])
        username_to_eras_playlist(form_data['prompt_text'])
        print("FINISHED PROCESSING")
        self.playlist_processing = False
        self.playlist_loaded = True
        return rx.redirect("/eras_page")

@rx.page(route="/")
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

@rx.page(route="/eras_page")
def eras_page() -> rx.Component:
    with open("song_list0.txt", 'r') as file:
        data1 = json.load(file)
    with open("song_list1.txt", 'r') as file:
        data2 = json.load(file)
    with open("song_list2.txt", 'r') as file:
        data3 = json.load(file)

    return rx.box(
        rx.box(
            rx.heading(f"{State.username}'s eras tour", size="7", align="center", style=dict(paddingBottom="2%", paddingTop="2%", color="white")),
            rx.text("using AI, we analyzed your instagram feed, discovered these eras of your life, and made playlists based off the vibe.", color="white", align="center", style=dict(paddingBottom="2%", paddingTop="0%")),
            background="rgba(0, 0, 0, 0.8)"
        ),
        rx.grid(
            rx.box(
                rx.heading(f"{data1[0]['vibe']} era", size="6", color="rgb(45, 42, 54)", align="center", style=dict(paddingBottom="3%", paddingTop="5%", maxWidth="70%", margin="0 auto")),
                rx.image(
                    src= f"/{State.username}-era1[0].jpg",
                    width="200px",
                    height="auto",
                    box_shadow="lg",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),
                rx.text(f"during this time of your life, you were {data1[0]['words'][0]}, {data1[0]['words'][1]}, {data1[0]['words'][2]}, {data1[0]['words'][3]}, {data1[0]['words'][4]}, {data1[0]['words'][5]}, {data1[0]['words'][6]}, and {data1[0]['words'][7]}", color="rgb(73, 67, 89)", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text(f"{data1[0]['songs'][0]['title']} - {data1[0]['songs'][0]['artist']}", align="center"),
                    rx.text(f"{data1[0]['songs'][1]['title']} - {data1[0]['songs'][1]['artist']}", align="center"),
                    rx.text(f"{data1[0]['songs'][2]['title']} - {data1[0]['songs'][2]['artist']}", align="center"),
                    rx.text(f"{data1[0]['songs'][3]['title']} - {data1[0]['songs'][3]['artist']}", align="center"),
                    rx.text(f"{data1[0]['songs'][4]['title']} - {data1[0]['songs'][4]['artist']}", align="center"),
                ),
            ),
            rx.box(
                rx.heading(f"{data2[0]['vibe']} era", size="6", color="rgb(45, 42, 54)", align="center", style=dict(paddingBottom="3%", paddingTop="5%", maxWidth="70%", margin="0 auto")),
                rx.image(
                    src= f"/{State.username}-era2[0].jpg",
                    width="200px",
                    height="auto",
                    box_shadow="5g",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),
                rx.text(f"you seem {data2[0]['words'][0]}, {data2[0]['words'][1]}, {data2[0]['words'][2]}, {data2[0]['words'][3]}, {data2[0]['words'][4]}, {data2[0]['words'][5]}, {data2[0]['words'][6]}, and {data2[0]['words'][7]} during this era", color="rgb(73, 67, 89)", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text(f"{data2[0]['songs'][0]['title']} - {data2[0]['songs'][0]['artist']}", align="center"),
                    rx.text(f"{data2[0]['songs'][1]['title']} - {data2[0]['songs'][1]['artist']}", align="center"),
                    rx.text(f"{data2[0]['songs'][2]['title']} - {data2[0]['songs'][2]['artist']}", align="center"),
                    rx.text(f"{data2[0]['songs'][3]['title']} - {data2[0]['songs'][3]['artist']}", align="center"),
                    rx.text(f"{data2[0]['songs'][4]['title']} - {data2[0]['songs'][4]['artist']}", align="center"),
                ),
            ),
            rx.box(
                rx.heading(f"{data3[0]['vibe']} era", size="6", color="rgb(45, 42, 54)", align="center", style=dict(paddingBottom="3%", paddingTop="5%", maxWidth="70%", margin="0 auto")),
                rx.image(
                    src= f"/{State.username}-era3[0].jpg",
                    width="200px",
                    height="auto",
                    box_shadow="lg",
                    style=dict(margin="0 auto", paddingBottom="3%")
                ),

                    rx.text(f"you're giving {data3[0]['words'][0]}, {data3[0]['words'][1]}, {data3[0]['words'][2]}, {data3[0]['words'][3]}, {data3[0]['words'][4]}, {data3[0]['words'][5]}, {data3[0]['words'][6]}, and {data3[0]['words'][7]}", color="rgb(73, 67, 89)", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
                    rx.box(
                    rx.text("songs", align="center", weight="bold", style=dict(paddingTop="3%")),
                    rx.text(f"{data3[0]['songs'][0]['title']} - {data3[0]['songs'][0]['artist']}", align="center"),
                    rx.text(f"{data3[0]['songs'][1]['title']} - {data3[0]['songs'][1]['artist']}", align="center"),
                    rx.text(f"{data3[0]['songs'][2]['title']} - {data3[0]['songs'][2]['artist']}", align="center"),
                    rx.text(f"{data3[0]['songs'][3]['title']} - {data3[0]['songs'][3]['artist']}", align="center"),
                    rx.text(f"{data3[0]['songs'][4]['title']} - {data3[0]['songs'][4]['artist']}", align="center"),
                ),
            ),
            columns="3",
            rows="1",
            width="100%",
            height="100%",
        ),
        height="100%",
        background="radial-gradient(circle, rgba(205,227,246,1) 1%, rgba(211,210,241,1) 25%, rgba(218,198,239,1) 45%, rgba(204,189,232,1) 61%, rgba(228,182,233,1) 80%, rgba(233,148,213,1) 100%)",
    )


app = rx.App()
app.add_page(index)
app.add_page(eras_page)