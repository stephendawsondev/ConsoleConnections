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


def main():
    """
    Run all program functions
    """
    print("Welcome to Console Connections\nThere's no cover to judge here!\n")
    user_data = establish_user_data()
    print(user_data)


main()
