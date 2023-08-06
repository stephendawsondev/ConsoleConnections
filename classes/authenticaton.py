import re


class Authentication():
    """
    Handles the password authentication and security questions.
    """

    def __init__(self):
        pass

    def prompt_for_password(self, new_or_existing_user, row=None):
        """
        Prompt the user for a password and validate it.\n
        - If the user is a new user, prompt them to create a password.\n
        - If the user is an existing user, prompt them to enter their password.\n
        - If the password is valid, return the password.\n
        - If the password is invalid, prompt the user to try again.
        """
        password_valid = False
        while password_valid is False:
            password_input = input("\nPlease enter your password:\n")
            password_valid = self.validate_password(password_input)
            if password_valid is True:
                if new_or_existing_user == "new":
                    return password_input
                if new_or_existing_user == "existing":
                    if password_input == row[1]:
                        print("\nPassword correct\n")
                        return password_input

                    print("\nPassword incorrect\n")
                    password_valid = False
                elif new_or_existing_user == "updating":
                    print("\nPassword updated\n")
                    return password_input

    def validate_password(self, password):
        """
        Checks the password length and complexity.\n
        - If the password is valid, return True.\n
        - If the password is invalid, return False.
        """
        # check for length between 8 to 32 characters
        if len(password) < 8 or len(password) > 32:
            print("\nPassword must be between 8 and 32 characters.\n")
            return False
        # regex for at least 1 digit and 1 symbol
        # https://www.freecodecamp.org/news/how-to-import-a-regular-expression-in-python/#howtousethepythonremodulewithregex
        if re.search(r"^(?=.*\d)(?=.*\W).*$", password):
            return True

        print("\nPassword must contain at least 1 digit and 1 symbol.\n")
        return False

    @staticmethod
    def prompt_for_security_questions():
        """
        User is given a list of 10 security questions to choose from.\n
        - User selects a question and provides an answer.
        - User is given the list of remaining questions and chooses one.
        - User provides an answer.
        - The questions and answers are returned in a list.
        """
        security_questions_and_answers = []

        security_question_list = [
            "What was the name of your first pet?",
            "In which town or city were you born?",
            "What was your favourite subject in secondary school?",
            "What is your mother's maiden name?",
            "What was the make and model of your first car?",
            "What is the first name of your best friend from childhood?",
            "In which city did your parents meet?",
            "What was the name of your primary school?",
            "What is your paternal grandfather's first name?",
            "What was the name of your first soft toy or plaything?"
        ]

        print("\nFor usercode/password recovery in the future, you will need to set some security questions.\nPlease choose from the list below:\n")
        for index, question in enumerate(security_question_list):
            print(f"{index+1}. {question}")

        while len(security_questions_and_answers) < 2:
            security_question_input = input(
                "\nPlease select a question by entering its number:\n")
            if not security_question_input.isdigit() or int(
                    security_question_input) < 1 or int(security_question_input) > 10:
                print("\nPlease enter a number between 1 and 10\n")
                continue
            security_question_input = int(security_question_input)
            security_question = security_question_list[security_question_input - 1]
            security_answer = input(
                f"\nPlease enter your answer to the question '{security_question}':\n")
            security_questions_and_answers.append(
                [security_question, security_answer])
            security_question_list.pop(security_question_input - 1)
            print("\nThank you. Please choose another question from the list below:\n")
            for index, question in enumerate(security_question_list):
                print(f"{index+1}. {question}")

        return security_questions_and_answers
