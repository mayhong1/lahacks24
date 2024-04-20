# for reusable UI components like buttons
import reflex as rx
from views import mouse_enters, mouse_leaves, NavBarState

state = NavBarState()

def navigation_bar():
    return rx.hstack(
        rx.button("Home", 
                  color_scheme="purple" if state.hovered == "Home" else "light-purple",
                  on_mouse_enter=lambda: mouse_enters(state, "Home"),
                  on_mouse_leave=lambda: mouse_leaves(state)
                  ),      
    
        rx.button("Playlist", 
                  color_scheme="purple" if state.hovered == "Playlist" else "light-purple",
                  on_mouse_enter=lambda: mouse_enters(state, "Playlist"),
                  on_mouse_leave=lambda: mouse_leaves(state)
                  ),

        rx.button("Settings", 
                  color_scheme="purple" if state.hovered == "Settings" else "light-purple",
                  on_mouse_enter=lambda: mouse_enters(state, "Settings"),
                  on_mouse_leave=lambda: mouse_leaves(state)
                 ),
            )



def hover_log_in_button(is_hovered=False):      #assign conditional value BEFORE parameter assignment
    if is_hovered:
        box_shadow_value="rgba(177, 156, 217) 0 15px 30px -10px" 
    else: box_shadow_value="rgba(151, 65, 252, 0.8) 0 15px 30px -10px" 
    return rx.button(
        "Log In",
        border_radius="1em", 
        box_shadow=box_shadow_value, 
        background_image="linear-gradient(144deg,#AF40FF,#5B42F3 50%,#00DDEB)",
        box_sizing="border-box", 
        color="white", 
        opacity=1, 
        _hover={"opacity": 0.5,}
    )

def click_log_in_button(is_clicked=False):
    if is_clicked:
        return rx.button(
            "Button Clicked"
        )
    else:
        return rx.button("Log In")
    




