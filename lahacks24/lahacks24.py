import json
import reflex as rx
from rxconfig import config
import reflex as rx
from vibe_generator import username_to_eras_playlist
from typing import List, Dict, Optional

# The app state
import json
from typing import List, Dict
# run 'pip install passlib' and 'pip install bcrypt==4.0.1'
import passlib.hash

from pymongo import MongoClient
from dotenv import load_dotenv
import reflex as rx
import os



docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"
load_dotenv()


# Set up the MongoDB connection
try:
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["retrotune"]
    users_collection = db["users"]
except Exception as e:
    print("Error connecting to MongoDB:", e)


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
    
    def to_index(self):
        return rx.redirect("/")
    
    def to_eras(self):
        return rx.redirect("/eras_page")
    
    def handle_login(self, form_data: dict):
        username = form_data.get('username')
        password = form_data.get('password')

        user = users_collection.find_one({"username": username})

        if user and passlib.hash.bcrypt.verify(password, user['password']):
            # Correct credentials, redirect to the index page
            print("Login successful!")
            return rx.redirect("/")
        else:
            # User not found or incorrect password, redirect to the signup page
            print("Incorrect username or password.")
            # Optionally, pass a message to the signup page indicating a failed login attempt
            return rx.redirect("/signup?error=login_failed")


    def handle_signup(self, form_data: dict):
        email = form_data.get('email')
        username = form_data.get('username')
        password = form_data.get('password')

        # Check if user exists
        if users_collection.find_one({"username": username}):
            print("User already exists.")
            # Redirect back to signup with an error message (implement error messaging in your actual app)
            return rx.redirect("/signup")
        
        # Hash the password before storing
        hashed_password = passlib.hash.bcrypt.hash(password)
        
        # Create user in the database
        db.users.insert_one({
            "email": email,
            "username": username,
            "password": hashed_password
        })
        print("User created successfully.")
        # Redirect to login page after successful signup
        return rx.redirect("/login")

# Homepage
@rx.page(route="/")
def index() -> rx.Component:

    home_playlist_settings = rx.center(
        rx.hstack(
            # rx.button("Home", 
            #     background_color=rx.color("pink", alpha=300),
            #     borderRadius="39%",
            #     size="4",
            #     margin="30px 0"
            # ), 
            rx.button("Playlist", 
                background_color=rx.color("pink", alpha=300),
                borderRadius="39%",
                size="4",
                margin="30px 0",
                on_click=State.to_eras
            ),
            # rx.button("Log Out", 
            #     background_color=rx.color("pink", alpha=300),
            #     borderRadius="39%",
            #     size="4",
            #     margin="30px 0"
            # ),
            justify="center",  # Center the buttons horizontally,
            spacing="3",
            width="100%", #need width="100%" twice for this to work 
            #on_click=State.to_logout
        ), 
        width="100%"
    )

    # RetroTune rounded box
    retrotune_box = rx.vstack(
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
        # rx.cond(
        #     State.playlist_processing,
        #     rx.chakra.circular_progress(is_indeterminate=True),
        # ),
        bg="white",
        padding="2em",
        align="center",
        borderRadius="10%",
        width="100%"
    )

    # Stack the elements vertically with home settings on top
    return rx.container(
        rx.vstack(
            home_playlist_settings,
            retrotune_box,
            width="100%",
            height="100vh",
            spacing="9",
        ),
        background="radial-gradient(circle, rgba(174,208,238,1) 0%, rgba(233,148,213,1) 100%)",
        size="1",
    )

# Playlists page
@rx.page(route="/eras_page")
def eras_page() -> rx.Component:
    return rx.box(
        rx.heading(f"{State.username}'s eras tour", size="7", align="center", style=dict(paddingBottom="2%", paddingTop="3%")),
        rx.text("Your Life, Your Music: Our AI has scanned your Instagram to craft playlists that echo the eras of your life.", align="center", style=dict(paddingBottom="2%", paddingTop="0%")),
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
                rx.text(f"your vibes: {State.data1[0]['words'][0]}, {State.data1[0]['words'][1]}, {State.data1[0]['words'][2]}, {State.data1[0]['words'][3]}, {State.data1[0]['words'][4]}, {State.data1[0]['words'][5]}, {State.data1[0]['words'][6]}, and {State.data1[0]['words'][7]}", style=dict(maxWidth="70%", margin="0 auto"), color="rgb(79, 83, 158)", align="center"),
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
                rx.text(f"your vibes: {State.data2[0]['words'][0]}, {State.data2[0]['words'][1]}, {State.data2[0]['words'][2]}, {State.data2[0]['words'][3]}, {State.data2[0]['words'][4]}, {State.data2[0]['words'][5]}, {State.data2[0]['words'][6]}, and {State.data2[0]['words'][7]} ", color="rgb(79, 83, 158)", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
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

                    rx.text(f"your vibes: {State.data3[0]['words'][0]}, {State.data3[0]['words'][1]}, {State.data3[0]['words'][2]}, {State.data3[0]['words'][3]}, {State.data3[0]['words'][4]}, {State.data3[0]['words'][5]}, {State.data3[0]['words'][6]}, and {State.data3[0]['words'][7]}", color="rgb(79, 83, 158)", style=dict(maxWidth="70%", margin="0 auto"), align="center"),
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
                "back",
                background_color=rx.color("pink", alpha=300),
                borderRadius="39%",
                size="4",
                margin="30px 0",
                on_click=State.to_index
            )
        ),
        height="100%",
        background="radial-gradient(circle, rgba(205,227,246,1) 1%, rgba(211,210,241,1) 25%, rgba(218,198,239,1) 45%, rgba(204,189,232,1) 61%, rgba(228,182,233,1) 80%, rgba(233,148,213,1) 100%)",

    )


@rx.page(route="log_out")
def log_out() -> rx.Component:
    return rx.container(
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

# Initialize website
app = rx.App()
app.add_page(index, route="/")
app.add_page(eras_page)