from classes.mixins import ClearTerminalMixin
from classes.user_access import UserAccess

CONSOLE_CONNECTIONS_HEADING = """

\t\t\t █▀▀█ █▀▀█ █▀▀▄ █▀▀ █▀▀█ █   █▀▀
\t\t\t █    █  █ █  █ ▀▀█ █  █ █   █▀▀
\t\t\t █▄▄█ ▀▀▀▀ ▀  ▀ ▀▀▀ ▀▀▀▀ ▀▀▀ ▀▀▀

\t\t█▀▀ █▀▀█ █▀▀▄ █▀▀▄ █▀▀ █▀▀ ▀▀█▀▀  ▀  █▀▀█ █▀▀▄ █▀▀
\t\t█   █  █ █  █ █  █ █▀▀ █     █   ▀█▀ █  █ █  █ ▀▀█
\t\t▀▀▀ ▀▀▀▀ ▀  ▀ ▀  ▀ ▀▀▀ ▀▀▀   ▀   ▀▀▀ ▀▀▀▀ ▀  ▀ ▀▀▀
"""


APP_SUBHEADING = "\t\t\t\u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764\n\n\t\t\tThere's no cover to judge here!\n\n\t\t\t\u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764\n"


class App():
    """
    The top level class for the app.
    - Starts the app
    """

    def __init__(self):
        self.start_app()

    ClearTerminalMixin.clear_terminal()

    def present_app_heading(self):
        """
        Displays the app heading.
        """
        print(
            f"{CONSOLE_CONNECTIONS_HEADING}\n{APP_SUBHEADING}")

    def start_app(self):
        """
        Starts the app.
        - Displays the app heading.
        - Establishes the user data.
        """
        user_access = UserAccess()
        self.present_app_heading()
        return user_access.establish_user_data()
