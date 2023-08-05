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
