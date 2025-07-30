# main.py
import flet as ft
import os
import sys

# --- Path Setup ---
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# --- Component Imports ---
from controllers.controller import Controller
from models.database import Database
from models.user import User
from models.skill import Skill
from models.request import Request
from models.session import Session
from models.learner_stats import LearnerStats
from models.practice_material import PracticeMaterial
from models.feedback import Feedback
from models.profile import Profile
from models.assignment import Assignment
from models.message import Message
from views.view import View

def main(page: ft.Page):
    """
    The main function to initialize and run the Flet application.
    """
    page.title = "Let's Ingles - English Proficiency Program"
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20
    
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.EXIT_TO_APP,
        on_click=lambda _: page.window_close(),
        tooltip="Exit Application",
        bgcolor=ft.Colors.RED_400
    )
    
    assets_dir = os.path.join(src_dir, "assets")
    page.assets_dir = assets_dir

    # --- Database and Model Initialization ---
    try:
        db_path = os.path.join(src_dir, "db", "LetsInglesDB.db")
        db = Database(db_file=db_path)
        
        models = {
            "user": User(db),
            "skill": Skill(db),
            "request": Request(db),
            "session": Session(db),
            "learner_stats": LearnerStats(db),
            "practice_material": PracticeMaterial(db),
            "feedback": Feedback(db),
            "profile": Profile(db),
            "assignment": Assignment(db),
            "message": Message(db)
        }
    except FileNotFoundError as e:
        page.add(ft.Text(f"Error: {e}", color="red"))
        return

    # --- MVC Initialization ---
    controller = Controller(models)
    view = View(controller)
    view.page = page
    controller.set_view(view)

    # --- Routing Logic ---
    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(view.get_splash_view())
        elif page.route == "/login":
            # This route is now handled by the splash screen logic
            page.go("/")
        elif page.route.startswith("/register"):
             # This route is now handled by the splash screen logic
            page.go("/")
        elif page.route == "/learner":
            if controller.current_user:
                page.views.append(view.get_learner_view())
            else:
                page.go("/")
        elif page.route == "/instructor":
            if controller.current_user:
                page.views.append(view.get_instructor_view())
            else:
                page.go("/")
        elif page.route == "/admin":
            if controller.current_user and controller.current_user['userRole'] == 'admin':
                page.views.append(view.get_admin_view())
            else:
                page.go("/")
        
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/")

if __name__ == "__main__":
    ft.app(target=main, assets_dir="src/assets")
