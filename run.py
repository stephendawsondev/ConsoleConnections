import gspread
from google.oauth2.service_account import Credentials
import re

# Define the scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Define the credentials
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ConsoleConnections')


def establish_user_data():
    """
    Establish if the user is a real user or a test user.\n
    - If a test user, pull data from the test user worksheet.\n
    - If a real user, pull data from the real user worksheet.
    """
    while True:
        user_type = input(
            "Are you just testing the app or here to find a connection?\n 1. Tester\n 2. Real User\n")

        if user_type == "1":
            print("Welcome to the test version - feel free to play around and make some connections with imaginary people.")
            # return data from test user worksheet (also breaks the loop)
            return SHEET.worksheet('test_users').get_all_values()
        elif user_type == "2":
            print("Welcome to the real version of the app")
            # return data from real user worksheet (also breaks the loop)
            return SHEET.worksheet('real_users').get_all_values()
        else:
            print("Please enter either '1' or '2' to continue")


def validate_password(password):
    # check for length between 8 to 32 characters
    if len(password) < 8 or len(password) > 32:
        print("Password must be between 8 and 32 characters")
        return False
    # regex for at least 1 digit and 1 symbol
    # https://www.freecodecamp.org/news/how-to-import-a-regular-expression-in-python/#howtousethepythonremodulewithregex
    if re.search(r"^(?=.*\d)(?=.*\W).*$", password):
        return True

    print("Password must contain at least 1 digit and 1 symbol")
    return False


def prompt_for_password(new_or_existing_user, row=None):
    """
    Prompt the user for a password and validate it.\n
    - If the user is a new user, prompt them to create a password.\n
    - If the user is an existing user, prompt them to enter their password.\n
    - If the password is valid, return the password.\n
    - If the password is invalid, prompt the user to try again.
    """
    password_valid = False
    while password_valid is False:
        password_input = input("Please enter your password:\n")
        password_valid = validate_password(password_input)
        if password_valid is True:
            if new_or_existing_user == "new":
                return password_input
            elif new_or_existing_user == "existing":
                if password_input == row[1]:
                    print("Password correct")
                    return password_input
                else:
                    print("Password incorrect")
                    password_valid = False


def user_login(data):
    """
    Checks if the user exists on the Google Sheet.\n
    - If the user exists, prompt them for password.\n
    - If the user doesn't exist, let them know and ask if they want to signup.\n
    """
    user_exists = False
    while user_exists is False:
        usercode_input = int(input("Please enter your usercode:\n"))
        # checks the first column of the data for the usercode
        for row in data:
            if row[0] == str(usercode_input):
                print("Usercode found")
                user_exists = True

                # prompt for password
                password = prompt_for_password("existing", row)
                if password is not None:
                    print("Login successful")
                    print(row)
                break
        else:
            print("Usercode not found")


def present_login_signup_step(data):
    """
    Provide the user with the option to login or signup.\n
    - If login, check if the user exists in the database and run the login function (if they exist)\n
    - If signup, check if the user exists in the database and run the signup function (if they don't exist).
    """
    while True:
        login_signup = input(
            "Would you like to login or signup? Please enter 1 or 2.\n 1. Login\n 2. Signup\n")

        if login_signup == "1":
            print("Login\n")
            # return data from login function (also breaks the loop)
            return user_login(data)
        elif login_signup == "2":
            print("Signup\n")
            # TODO: Create signup function that checks if the user exists in the database and adds them if they don't exist
            # return data from signup function (also breaks the loop)
            return signup(data)
        else:
            print("Please enter either '1' to Login or '2' to Signup\n")


def main():
    """
    Run all program functions
    """
    print("Welcome to Console Connections\nThere's no cover to judge here!\n")
    user_data = establish_user_data()
    present_login_signup_step(user_data)


main()
