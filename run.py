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


def establish_user_type():
    """
    Establish if the user is a real user or a test user
    """
    user_type = input(
        "Are you just testing the app or here to find a connection?\n 1. Tester\n 2. Real User\n")

    if user_type == "1":
        print("Welcome to the test version - feel free to play around and make some connections with imaginary people.")
    elif user_type == "2":
        print("Welcome to the user version of the app")
    else:
        print("Please enter either 'test' or 'user' to continue")


def main():
    """
    Run all program functions
    """
    establish_user_type()


main()
