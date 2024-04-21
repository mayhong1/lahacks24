from rxconfig import config
from vibe_generator import username_to_eras_playlist
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
    client = MongoClient(os.getenv("MONGODB_URI"))
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
    """The app state."""


    image_url="alicewang10t-era1[0].jpg"
    username=""
    playlist_processing = False
    playlist_loaded = False

    data1: List[Dict[str, List[Dict[str, str]]]] = {}
    data2: List[Dict[str, List[Dict[str, str]]]] = {}
    data3: List[Dict[str, List[Dict[str, str]]]] = {}
    
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

        with open("song_list0.txt", 'r') as file:
            self.data1 = json.load(file)
        with open("song_list1.txt", 'r') as file:
            self.data2 = json.load(file)
        with open("song_list2.txt", 'r') as file:
            self.data3 = json.load(file)


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
            # rx.cond(
            #     State.playlist_processing,
            #     rx.chakra.circular_progress(is_indeterminate=True),
            # ),
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



@rx.page(route="/login")
def login_page() -> rx.Component:
    # Create a centered box to hold the form
    return rx.center(
        rx.box(
            # Stack elements vertically: heading, form, and button
            rx.heading("Login", size="4", style={"margin-bottom": "10px"}),
            rx.form(
                rx.vstack(
                    # Input for username
                    rx.input(id="username", placeholder="Username", size="3"),
                    # Input for password
                    rx.input(id="password", placeholder="Password", type="password", size="3"),
                    # Submit button
                    rx.button("Login", type="submit", size="3")
                ),
                # Define what happens on form submission
                on_submit=State.handle_login,
                # Set the width of the form
                width="100%"
            ),
            # Style the box
            bg="white",
            padding="2em",
            align="center",
            # Set the width of the box
            width="25em"
        ),
        # Style the background of the center component
        background="linear-gradient(120deg, #a6c0fe 0%, #f68084 100%)",
        # Set the full height of the viewport
        height="100vh",
        # Set the full width of the viewport
        width="100%"
    )


@rx.page(route="/signup")
def signup_page() -> rx.Component:
    """Page to sign up a new user."""
    return rx.center(
        rx.box(
            rx.heading("Sign Up", size="4", style={"margin-bottom": "10px"}),
            rx.text("Please provide information below!", style={"margin-bottom": "10px"}),
            rx.form(
                rx.vstack(
                    rx.input(id="email", placeholder="Email", size="3"),
                    rx.input(id="username", placeholder="Username", size="3"),
                    rx.input(id="password", placeholder="Password", type="password", size="3"),
                    rx.button("Create Account", type="submit", size="3"),
                ),
                on_submit=State.handle_signup,
                width="100%",
            ),
            bg="white",
            padding="2em",
            align="center",
            width="25em",
        ),
        background="linear-gradient(120deg, #a6c0fe 0%, #f68084 100%)",
        height="100vh",
        width="100%",
    )


app = rx.App()
app.add_page(index, route="/")
app.add_page(eras_page)
app.add_page(login_page, route="/login")
app.add_page(signup_page, route="/signup")

