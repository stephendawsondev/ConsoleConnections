from classes.profile import Profile
from classes.quiz import Quiz
from classes.mixins import ClearTerminalMixin
from classes.matcher import Matcher
from classes.message import Message


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

        ClearTerminalMixin.clear_terminal()
        while True:
            main_menu_input = input(
                "\nPlease select the number of what you want to do.\n\n1. Compatibility quiz\t 2. Edit profile\t 3. View top matches\t 4. View messages\t 5. Logout\n")

            if main_menu_input == "1":
                print("\nCompatibility quiz\n")
                quiz = Quiz(user, self.present_main_menu)
                return quiz.present_compatibility_quiz()

            if main_menu_input == "2":
                print("\nEdit profile\n")
                profile = Profile(user,
                                  self.present_main_menu)
                return profile.present_edit_profile()

            if main_menu_input == "3":
                print("\nView top matches\n")
                # return data from view top matches functioth
                matcher = Matcher(user, self.present_main_menu)
                return matcher.view_top_matches()

            if main_menu_input == "4":
                print("\nView messages\n")
                # return data from view messages function
                message = Message(user, self.present_main_menu)
                return message.view_all_messages()

            if main_menu_input == "5":
                # log user out and present login/signup screen
                print("\Logged out\n")
                from classes.user_access import UserAccess
                user_access = UserAccess()
                return user_access.present_login_signup_step()

            print("\nPlease enter a number between 1 and 5\n")
