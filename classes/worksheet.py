"""
The Worksheet class is responsible for handling the worksheet operations.
- Pull data from worksheet.
- Write data to worksheet.
- Edit worksheet data.
"""
import re
import json
import warnings
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

    def __init__(self):
        pass

    worksheet_selected = None

    @classmethod
    def set_worksheet(cls, worksheet):
        """
        Class method to update the worksheet.
        Removes the need to pass the worksheet as an argument.
        """
        cls.worksheet_selected = worksheet

    def get_all_values(self):
        """
        Pulls all values from the worksheet.
        """
        return SHEET.worksheet(
            self.__class__.worksheet_selected).get_all_values()

    def add_user(self, user):
        """
        Appends a user to the selected worksheet.
        """
        selected_worksheet = (self.__class__.worksheet_selected
                              if self.__class__.worksheet_selected
                              is not None else
                              self.__class__.worksheet_selected)
        SHEET.worksheet(selected_worksheet).append_row(
            [
                user.usercode,
                user.password,
                user.alias,
                str(user.security_questions_and_answers),
                user.age,
                user.gender,
                None,
                str([]),
                str(user.age_range_seeking),
                None,
                None,
                None,
                user.row_num
            ])

    def update_cell(self, row, column, value):
        """
        Updates a cell in the worksheet.
        """
        SHEET.worksheet(self.__class__.worksheet_selected).update_cell(
            row, column, value)

    def update_row(self, row, values):
        """
        Updates an entire row in the worksheet.
        """
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', category=UserWarning)
            SHEET.worksheet(self.__class__.worksheet_selected).update(
                f"A{row}:M{row}", [values])

    def get_user_messages(self, user):
        """
        Gets the messages in a user's messages cell.
        """
        if isinstance(user, list):
            user_messages = SHEET.worksheet(
                self.__class__.worksheet_selected).cell(
                user[12], 10).value
        else:
            user_messages = SHEET.worksheet(
                self.__class__.worksheet_selected).cell(
                user.row_num, 10).value

        # check if user messages is an empty string, None or an empty list
        messages = user_messages
        if messages == "" or messages is None or messages == "[]":
            return []
        if isinstance(messages, list):
            return messages

        # replace single quote marks around words with double quotes
        # but keep single quote marks within works
        messages = re.sub(
            r"(?<![\w\\])'|'(?![\w\\])", "\"", messages)
        messages = json.loads(messages)

        # sort messages by last_message_received_timestamp (most recent
        # first)
        for message in messages:
            message[2].sort(key=lambda x: x[2], reverse=True)

        return messages
