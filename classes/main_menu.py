"""
This module contains the MainMenu class, which handles
the main menu screen and the actions that can be taken
after a user has logged in.
"""
from colorama import Fore, init
from classes.profile import Profile
from classes.quiz import Quiz
from classes.mixins import ClearTerminalMixin
from classes.matcher import Matcher
from classes.message import Message


init(autoreset=True)


class MainMenu():
    """
    Handles displaying the menu screen and the actions
    actions that can be taken after a user has logged in.
    """

    def __init__(self):
        pass

    def present_main_menu(self, user=None):
        """
        Present the user with the main menu options.
        - If the user selects '1', run the compatibility quiz.
        - If the user selects '2', run the edit profile function.
        - If the user selects '3', run the view top matches function.
        - If the user selects '4', run the view messages function.
        - If the user selects '5', run the logout function.
        """
        print(f"{Fore.YELLOW}Main Menu\n")
        while True:
            main_menu_input = input("\nPlease select the number of the"
                                    " action you want to take:"
                                    "\n\n1. Compatibility quiz"
                                    "     2. Edit profile"
                                    "     3. View top matches"
                                    "\n\n\t\t4. View messages"
                                    "     5. Logout\n")

            if main_menu_input == "1":
                ClearTerminalMixin.clear_terminal()
                quiz = Quiz(user, self.present_main_menu)
                return quiz.present_compatibility_quiz()

            if main_menu_input == "2":
                ClearTerminalMixin.clear_terminal()
                profile = Profile(user,
                                  self.present_main_menu)
                return profile.present_edit_profile()

            if main_menu_input == "3":
                ClearTerminalMixin.clear_terminal()
                # return data from view top matches function
                matcher = Matcher(user, self.present_main_menu)
                return matcher.view_top_matches()

            if main_menu_input == "4":
                ClearTerminalMixin.clear_terminal()
                print(f"{Fore.YELLOW}View all messages\n")
                # return data from view messages function
                message = Message(user, self.present_main_menu)
                return message.view_all_messages()

            if main_menu_input == "5":
                ClearTerminalMixin.clear_terminal()
                # log user out and present login/signup screen
                print(f"{Fore.GREEN}Logged out\n")
                ClearTerminalMixin.clear_terminal(2)
                from classes.user_access import UserAccess
                user_access = UserAccess()
                return user_access.present_login_signup_step()

            print(f"{Fore.RED}\nPlease enter a number between 1 and 5\n")
