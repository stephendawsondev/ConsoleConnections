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


class Worksheet():
    """
    Responsible for handling the worksheet operations.
    - Pull data from worksheet.
    - Write data to worksheet.
    - Edit worksheet data.
    """

    def __init__(self, worksheet):
        self.worksheet = worksheet

    def get_all_values(self):
        """
        Pulls all values from the worksheet.
        """
        return SHEET.worksheet(self.worksheet).get_all_values()

    def add_user(self, user):
        """
        Appends a user to the selected worksheet.
        """
        SHEET.worksheet(self.worksheet).append_row([user.usercode, user.password, user.alias, str(
            user.security_questions_and_answers), user.age, user.gender, None, None, None, None, None, None, user.row_num])

    def update_cell(self, row, column, value):
        """
        Updates a cell in the worksheet.
        """
        SHEET.worksheet(self.worksheet).update_cell(row, column, value)

    def update_row(self, row, values):
        """
        Updates an entire row in the worksheet.
        """
        SHEET.worksheet(self.worksheet).update(f"A{row}:M{row}", [values])