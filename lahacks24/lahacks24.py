from rxconfig import config
from vibe_generator import username_to_eras_playlist

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


class State(rx.State):
    """The app state."""

    def generate_playlist(self, form_data: dict):
        self.form_data = form_data
        print(form_data['prompt_text'])
        username_to_eras_playlist(form_data['prompt_text'])

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
        width="25em",
        bg="white",
        padding="2em",
        align="center",
    ),
    width="100%",
    height="100vh",
    background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
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

