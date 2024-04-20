#this will work with components.py to allow users to interact w/ the webapp
import reflex as rx
from reflex import State, Component, html
import components

class NavBarState(State):
    def __init__(self):
        super().__init__() #ensures proper initialization of base class
        self.hovered = None  #tracks which button is hovered, initially None

    def currently_hovered_button(self, hover_button):
        self.hovered = hover_button

    def clear_hover(self):
        self.hovered = None


def mouse_enters(state, hover_button):
    state.currently_hovered_button(hover_button)

def mouse_leaves(state):
    state.clear_hover()


class LogInClick(State):
    def __init__(self):
        super().__init__()
        self.clicked = None
    
    def currently_clicked_button(self, clicking_button):
        self.clicked = clicking_button

    def clear_clicked_button(self):
        self.clicked = None


class LogInHover(State):
    def __init__(self):
        super().__init__()
        self.hovered = None
    def currently_hovered_button(self, hover_button):
        self.hovered = hover_button

    def clear_hover(self):
        self.hovered = None

def log_in_mouse_enters(state, hover_button):
    state.currently_hovered_button(hover_button)

def log_in_mouse_leaves(state):
    state.clear_hover()
