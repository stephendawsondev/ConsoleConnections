import datetime
import gspread
from classes.worksheet import Worksheet


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

        print("\nDisplay messages\n")
        worksheet = Worksheet()
        user_messages = worksheet.get_user_messages(self.user)

        if len(user_messages) > 0:
            for message in user_messages:
                if message[0] == match[0]:
                    messages = message[2]
                    break

        if len(messages) == 0:
            print(f"\nYou have no messages with {match[2]}.\n")

        if len(messages) > 0:
            # sort messages by most recent first
            messages.sort(key=lambda x: x[2], reverse=True)

            for message in messages:
                [message_text, user_sent, timestamp] = message
                if user_sent == "True":
                    print(f"\n{timestamp} - {self.user.alias}: {message_text}\n")
                else:
                    print(f"\n{timestamp} - {match[2]}: {message_text}\n")

        while True:
            user_input = input(
                "\nWould you like to 1. Send a message or 2. Go back ?\n")
            if user_input == "1":
                return self.send_message(user_messages, messages, match)
            if user_input == "2":
                return self.callback(self.user)
            print("\nPlease enter either '1' or '2'\n")

    def send_message(self, all_user_messages, messages_to_match, match):
        """
        Sends a message to the match.
        The messages are timestamped and then added to the user
        and match messages cell in the worksheet.
        """
        user_message = input("\nPlease enter your message:\n")

        # get current timestamp
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        print(f"all user messages before: {all_user_messages}")

        print("\n", timestamp, user_message)

        print("\nMessages to match (before):\n", messages_to_match)

        # add message to user's messages
        try:
            messages_to_match.insert(0, [user_message, "True", timestamp])
        except Exception as excep:
            print("\nError adding message to user's messages\n")
            print(excep)

        print("\nMessages to match (after):\n", messages_to_match)

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

        print("\nAll user messages (after):\n", all_user_messages)

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

        print("\nAll match messages (before):\n", all_match_messages)

        # add message to match's messages
        found_user_match = False
        for message in all_match_messages:
            if message[0] == self.user.usercode:
                message[2].insert(0, [user_message, "False", timestamp])
                found_user_match = True
                break

        if not found_user_match:
            all_match_messages.insert(
                0, [self.user.usercode, timestamp, [[user_message, "False", timestamp]]])

        print("\nAll match messages (after):\n", all_match_messages)

        # update match's messages cell
        try:
            worksheet.update_cell(match[12], 10, str(all_match_messages))
        except Exception as excep:
            print("\nError updating match's messages cell\n")
            print(excep)

        print("\nMessage sent!\n")

        return self.callback(self.user)
