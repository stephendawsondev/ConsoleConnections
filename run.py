import gspread
from google.oauth2.service_account import Credentials

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
            # TODO: Create login function that checks if the user exists in the database
            # return data from login function (also breaks the loop)
            return login(data)
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
    print(user_data)


main()
