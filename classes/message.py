"""
Module providing data/time functionality
for timestamps in the message class.
"""
import datetime
import gspread
from colorama import init, Fore
from classes.worksheet import Worksheet
from classes.mixins import ClearTerminalMixin

init(autoreset=True)


class Message():
    """
    Handles the displaying and sending of messages between users.
    """

    def __init__(self, user, callback):
        self.user = user
        self.callback = callback

    def display_messages(self, match):
        """
        Displays the messages between the user and their match.
        """

        messages = []

        worksheet = Worksheet()
        user_messages = worksheet.get_user_messages(self.user)

        if len(user_messages) > 0:
            for message in user_messages:
                if message[0] == match[0]:
                    messages = message[2]
                    break

        if len(messages) == 0:
            print(f"\nYou have no messages with {match[2]}.\n")

            ClearTerminalMixin.clear_terminal(2)
        if len(messages) > 0:
            print(f"""
Your messages are in {Fore.CYAN}CYAN{Fore.WHITE}
and your match's messages are in {Fore.LIGHTMAGENTA_EX}PURPLE{Fore.WHITE}.
""")
            # sort messages by most recent first
            messages.sort(key=lambda x: x[2], reverse=True)

            for message in messages:
                [message_text, user_sent, timestamp] = message
                if user_sent == "True":
                    print(f"""{Fore.CYAN}
{timestamp} - {self.user.alias}: {message_text}
""")
                else:
                    print(f"""{Fore.LIGHTMAGENTA_EX}
{timestamp} - {match[2]}: {message_text}
""")

        while True:
            user_input = input("""
Would you like to send a message or go back to the main menu?
1. Send message     2. Go back to messages
""")
            if user_input == "1":
                return self.send_message(user_messages, messages, match)
            if user_input == "2":
                print("\nReturning to main menu...\n")
                ClearTerminalMixin.clear_terminal(2)
                return self.callback(self.user)
            print(f"{Fore.RED}\nPlease enter either '1' or '2'.\n")

    def send_message(self, all_user_messages, messages_to_match, match):
        """
        Sends a message to the match.
        The messages are timestamped and then added to the user
        and match messages cell in the worksheet.
        """
        user_message = input("\nPlease enter your message:\n")

        # get current timestamp
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # add message to user's messages
        try:
            messages_to_match.insert(0, [user_message, "True", timestamp])
        except AttributeError as excep:
            print("\nError adding message to user's messages\n")
            print(excep)

        # add messages_to_match to all_user_messages
        found_match = False
        for message in all_user_messages:
            if message[0] == match[0]:
                message[2] = messages_to_match
                found_match = True
                break

        if not found_match:
            all_user_messages.insert(
                0, [match[0], timestamp, messages_to_match])

        # update user's messages cell
        try:
            worksheet = Worksheet()
            worksheet.update_cell(self.user.row_num, 10,
                                  str(all_user_messages))
        except gspread.exceptions.APIError as excep:
            print("\nError updating user's messages cell\n")
            print(excep)

        # add message to match's messages
        worksheet = Worksheet()
        all_match_messages = worksheet.get_user_messages(match)

        # add message to match's messages
        found_user_match = False
        for message in all_match_messages:
            if message[0] == self.user.usercode:
                message[2].insert(0, [user_message, "False", timestamp])
                found_user_match = True
                break

        if not found_user_match:
            all_match_messages.insert(0, [self.user.usercode, timestamp, [
                [user_message, "False", timestamp]]])

        # update match's messages cell
        try:
            worksheet.update_cell(match[12], 10, str(all_match_messages))
        except gspread.exceptions.APIError as excep:
            print("\nError updating match's messages cell\n")
            print(excep)

        print(f"{Fore.GREEN}\nMessage sent!\n")

        ClearTerminalMixin.clear_terminal(2)

        return self.display_messages(match)

    def view_all_messages(self):
        """
        Displays the latest message from each match for the user.
        """
        worksheet = Worksheet()
        user_messages = worksheet.get_user_messages(self.user)

        if len(user_messages) == 0:
            print("\nYou have no messages.\n")
            ClearTerminalMixin.clear_terminal(2)
            return self.callback(self.user)

        worksheet = Worksheet()
        all_users = worksheet.get_all_values()
        matches = []
        for message in user_messages:
            for user in all_users:
                if message[0] == user[0]:
                    matches.append(user)
                else:
                    continue

        for index, message in enumerate(user_messages, start=1):

            for match in matches:
                if match[0] == message[0]:
                    match_alias = match[2]
                    last_message_text = ""
                    last_message_date = message[1]
                    # loop through match messages to check for the
                    # last message where user_sent is false
                    for match_message in message[2]:
                        if match_message[1] == "False":
                            last_message_date = match_message[2]
                            message[1] = last_message_date
                            last_message_text = match_message[0]
                            break
                    print(f"""
{index}. Latest message from {match_alias}: {last_message_text}
Received: {message[1]}

*************************************
""")
        while True:
            user_input = input("""
Would you like to view all of a match's messages or go back?
1. View all of a match's messages     2. Go back
""")
            if user_input == "1":
                match_number = input("""
Please enter the number of the match you would like to view:
""")
                try:
                    match_number = int(match_number)
                except ValueError:
                    print(f"{Fore.RED}\nPlease enter a number\n")
                    continue
                if match_number < 1 or match_number > len(matches):
                    print(f"""{Fore.RED}
Please enter a number between 1 and {len(matches)}
""")
                    continue
                ClearTerminalMixin.clear_terminal()
                return self.display_messages(matches[match_number - 1])
            if user_input == "2":
                ClearTerminalMixin.clear_terminal()
                print("\nReturning to main menu...\n")
                ClearTerminalMixin.clear_terminal(2)
                return self.callback(self.user)
            print(f"{Fore.RED}\nPlease enter either '1' or '2'\n")
