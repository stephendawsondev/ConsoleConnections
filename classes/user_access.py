"""
The User Access class is responsible for handling the sheet selection,
and pulling data from the selected sheet.
Also handles user signup and login.
"""
import random
from classes.worksheet import Worksheet
from classes.profile import Profile
from classes.authenticaton import Authentication
from classes.user import User
from classes.mixins import ClearTerminalMixin
from classes.main_menu import MainMenu


class UserAccess():
    """
    Responsible for handling the sheet selection,
    and pulling data from the selected sheet.
    Also handles user signup and login.
    """

    def __init__(self):
        pass

    def establish_user_data(self):
        """
        Establish if the user is a real user or a test user.
        - If a test user, pull data from the test user worksheet.
        - If a real user, pull data from the real user worksheet.
        """

        while True:

            user_type = input(
                """
Are you testing or here to find a connection? Please enter 1 or 2.

1. Tester     2. Real User
""")

            if user_type == "1":
                print("""
Welcome to the test version of the app - feel free to play
around and make some connections with imaginary people.
""")

                Worksheet.set_worksheet("test_users")
                break

            elif user_type == "2":
                print("""
Welcome to the real version of the app - let's make some connections!
""")
                Worksheet.set_worksheet("real_users")
                break

            else:
                print("\nPlease enter either '1' or '2' to continue.\n")

        return self.present_login_signup_step()

    def user_signup(self, user_data):
        """
Runs generate usercode, password, alias and security question functions.
- Adds the user to the Google sheet."""

        usercode = self.generate_random_usercode(user_data)

        print(
            f"""
If you complete the signup process, your usercode will be {usercode}.
Please keep this safe as you will need it to login.
""")

        authentication = Authentication()
        password = authentication.prompt_for_password("new")

        alias = self.create_and_validate_alias(user_data)

        ClearTerminalMixin.clear_terminal()

        print("Great! We've got your username, password and alias!\n")

        auth_check = Authentication.prompt_for_security_questions()
        security_questions_and_answers = auth_check

        ClearTerminalMixin.clear_terminal()

        print("\nSecurity questions added!\n")

        age = Profile.prompt_for_age()

        ages_seeking = Profile.set_age_range_seeking()

        gender = Profile.prompt_for_gender()

        row_num = len(user_data) + 1

        # create user object
        user = User(
            usercode,
            password,
            alias,
            security_questions_and_answers,
            age,
            gender,
            None,
            None,
            ages_seeking,
            None,
            None,
            None,
            row_num)

        # add user to Google Sheet
        selected_worksheet = Worksheet()
        selected_worksheet.add_user(user)

        ClearTerminalMixin.clear_terminal()
        print(f"\nSignup successful! Remember, your usercode is {usercode}.\n")

        main_menu = MainMenu()

        return main_menu.present_main_menu(user)

    def generate_random_usercode(self, user_data):
        """
        - Generates a new 6-digit usercode for the user.\n
        - Checks if the usercode already exists in the database.\n
        - If the usercode exists, generate a new one.\n
        """
        usercode = random.randint(100000, 999999)

        # check if the usercode already exists in the database
        for row in user_data:
            if row[0] == str(usercode):
                # if the usercode exists, generate a new one
                self.generate_random_usercode(user_data)
        return usercode

    def create_and_validate_alias(self, user_data):
        """
        Checks the user's alias against the Google Sheet.
        - Make sure the alias is no more than 16 characters.
        - If the alias exists, prompt the user to come up with a new alias.
        - If the alias doesn't exist, return the alias.
        """
        alias = input("""
You will also need to create an alias to use for in-app communication.
The alias must be unique and it is recommended that it does not easily
identify you (for security reasons).

Please enter your alias now:
""")

        # check if the alias is greater than 3 but fewer than 16 characters
        while len(alias) < 3 or len(alias) > 16:
            alias = input("""
Alias must be greater than 3 but fewer than 16 characters. Please try again:
""")

        # check if the alias already exists in the database
        for row in user_data:
            if row[2] == alias:
                # if the alias exists, prompt the user to come up with a new
                # alias
                print("\nAlias already exists.\n")
                return self.create_and_validate_alias(user_data)
        return alias

    def user_login(self, all_users):
        """
Checks if the user exists on the Google Sheet.\n
- If the user exists, prompt them for password.\n
- If the user doesn't exist, let them know and ask if they want to signup.\n
        """
        all_users = Worksheet().get_all_values()
        user_exists = False
        while user_exists is False:
            usercode_input = input("\nPlease enter your usercode:\n")
            # checks the first column of the data for the usercode
            for index, row in enumerate(all_users):
                if row[0] == str(usercode_input):
                    user_exists = True
                    # prompt for password
                    authentication = Authentication()
                    password = authentication.prompt_for_password(
                        "existing", row)
                    if password is not None:
                        print("\nLogin successful\n")
                        user = User(
                            row[0],
                            row[1],
                            row[2],
                            row[3],
                            row[4],
                            row[5],
                            row[6],
                            row[7],
                            row[8],
                            row[9],
                            row[10],
                            row[11],
                            index + 1)

                        ClearTerminalMixin.clear_terminal(2)
                        main_menu = MainMenu()
                        return main_menu.present_main_menu(user)
                    break
            else:
                print("\nUsercode not found.\n")

    def present_login_signup_step(self):
        """
Provide the user with the option to login or signup.\n
- If login, check if the user exists in the database and
run the login function (if they exist)
- If signup, check if the user exists in the database
and run the signup function (if they don't exist).
        """
        while True:
            login_signup = input("""
Would you like to login or signup? Please enter 1 or 2.

1. Login     2. Signup
""")

            all_users = Worksheet().get_all_values()
            if login_signup == "1":
                ClearTerminalMixin.clear_terminal()
                print("\nLogin\n")
                # return data from login function (also breaks the loop)
                return self.user_login(all_users)
            if login_signup == "2":
                ClearTerminalMixin.clear_terminal()
                print("\nSignup\n")
                # return data from signup function (also breaks the loop)
                return self.user_signup(all_users)

            print("\nPlease enter either '1' to Login or '2' to Signup.\n")
