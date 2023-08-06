"""
The Authentication class is responsible for handling the password
authentication and security questions.
"""
import re


class Authentication():
    """
    Handles the password authentication and security questions.
    """

    def __init__(self):
        pass

    def prompt_for_password(self, new_or_existing_user, row=None):
        """
        Prompt the user for a password and validate it.
        - If the user is a new user, prompt them to create a password.
        - If the user is an existing user, prompt them to enter their password.
        - If the password is valid, return the password.
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
                        return password_input
                    print("\nIncorrect password\n")
                    password_valid = False
                elif new_or_existing_user == "updating":
                    print("\nPassword updated\n")
                    return password_input

    def validate_password(self, password):
        """
        Checks the password length and complexity.
        - If the password is valid, return True.
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
        User is given a list of 10 security questions to choose from.
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

        print("""
For credential recovery, you will need to set some security questions.
Please choose from the list below:
""")
        for index, question in enumerate(security_question_list):
            print(f"{index+1}. {question}")

        while len(security_questions_and_answers) < 2:
            security_question = input(
                "\nPlease select a question by entering its number:\n")

            try:
                security_question = int(security_question)
                if 1 <= security_question <= len(security_question_list):
                    selected_question = security_question_list.pop(
                        security_question - 1)
                    security_answer = input(f"""
Please enter your answer to the question '{selected_question}':
""")
                    security_questions_and_answers.append(
                        [selected_question, security_answer])

                    print("""
Thank you. Please choose another question from the list below:
""")
                    for index, question in enumerate(security_question_list):
                        print(f"{index+1}. {question}")
                else:
                    print("""
Please enter a number between 1 and the number of remaining questions
""")
            except ValueError:
                print("\nInvalid input. Please enter a number.\n")

        return security_questions_and_answers
