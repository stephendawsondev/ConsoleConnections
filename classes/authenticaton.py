"""
The Authentication class is responsible for handling the password
authentication and security questions.
"""
import json
import re
from colorama import Fore, init
from classes.worksheet import Worksheet
from classes.mixins import ClearTerminalMixin

init(autoreset=True)


class Authentication():
    """
    Handles the password authentication and security questions.
    """

    def __init__(self, credential, callback):
        self.credential = credential
        self.callback = callback

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
            if new_or_existing_user == "existing":
                password_input = input("\nPlease enter your password or press "
                                       "'f' if you forgot it:\n")

                if password_input == "f":
                    self.credential = "password"
                    return self.recover_credentials(row)
            else:
                password_input = input("\nPlease enter your new password:\n")

            password_valid = self.validate_password(password_input)
            if password_valid is True:
                if new_or_existing_user == "new":
                    return password_input
                if new_or_existing_user == "existing":
                    if password_input == row[1]:
                        return password_input
                    print(f"{Fore.RED}\nIncorrect password\n")
                    password_valid = False
                elif new_or_existing_user == "updating":
                    print(f"{Fore.GREEN}Password updated\n")
                    return password_input

    def validate_password(self, password):
        """
        Checks the password length and complexity.
        - If the password is valid, return True.
        - If the password is invalid, return False.
        """
        # check for length between 8 to 32 characters
        if len(password) < 8 or len(password) > 32:
            print(f"{Fore.RED}\n"
                  "Password must be between 8 and 32 characters.\n")
            return False
        # regex for at least 1 digit and 1 symbol
        # https://www.freecodecamp.org/news/
        # how-to-import-a-regular-expression-in-python
        # /#howtousethepythonremodulewithregex
        if re.search(r"^(?=.*\d)(?=.*\W).*$", password):
            return True

        print(f"{Fore.RED}\n"
              "Password must contain at least 1 digit and 1 symbol.\n")
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

        print("For credential recovery, you will need to set"
              " some security questions.\n"
              "Please choose from the list below:\n")

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
                    security_answer = input("\nPlease enter your "
                                            "answer to the question"
                                            f" '{selected_question}':\n")

                    if security_answer == "":
                        print(f"{Fore.RED}\nPlease enter an answer.")
                        continue
                    security_questions_and_answers.append(
                        [selected_question, security_answer])

                    print("Thank you. Please choose another "
                          "question from the list below:")
                    for index, question in enumerate(security_question_list):
                        print(f"{index+1}. {question}")
                else:
                    print(f"{Fore.RED}\nPlease enter a number "
                          "between 1 and the number of remaining questions.")
            except ValueError:
                print(f"{Fore.RED}\nPlease enter a number.")

        return security_questions_and_answers

    def recover_credentials(self, row=None):
        """
        Method to recover forgotten usercode or
        password.
        - If they forgot their usercode, prompts the user for their alias.
        - If they don't know the alias, lets them know they cannot recover
        their account and asks if they want to sign up.
        - If they know the alias, prompts them for their alias
        and asks them to answer their security questions.
        - If they forgot their password, prompts the user for their usercode.
        - If they don't know their usercode, asks them if they want to recover
        their usercode and run recover_credentials again, with usercode param.
        """
        all_users = Worksheet().get_all_values()
        if self.credential == "usercode":
            alias = input(
                "\nPlease enter your alias. If you forgot it, enter 'f': \n")
            if alias == "f":
                print(
                    f"{Fore.RED}\nIf you forgot your alias. "
                    "You will need to sign up again.\n")

                ClearTerminalMixin.clear_terminal(2)
                return self.callback()
            user_exists = False
            selected_row = None
            while user_exists is False:
                for row in all_users:
                    if row[2] == alias:
                        user_exists = True
                        selected_row = row
                        break
                if user_exists is False:
                    print(f"{Fore.RED}\nAlias does not exist. "
                          "Please try again.\n")
                    return self.recover_credentials()

                if Authentication.verify_security_answers(selected_row):
                    print(f"{Fore.GREEN}\nYour usercode is "
                          f"{selected_row[0]}.\n")
                    return self.callback()

                print(f"{Fore.RED}\nYou have failed to answer "
                      "your security questions correctly.")
                return self.callback()

        if self.credential == "password":
            usercode = row[0]

            user_exists = False
            selected_row = None
            while user_exists is False:
                for row in all_users:
                    if row[0] == usercode:
                        user_exists = True
                        selected_row = row
                        break
                if user_exists is False:
                    print(f"{Fore.RED}\nUsercode does not exist. "
                          "Please try again.\n")
                    return self.recover_credentials()
                questions_correct = Authentication.verify_security_answers(
                    selected_row)
                if questions_correct is True:

                    new_password = self.prompt_for_password(
                        "updating", selected_row)
                    worksheet = Worksheet()
                    worksheet.update_cell(selected_row[12], 2, new_password)
                    return self.callback()
                print(f"{Fore.RED}\nYou have failed to answer "
                      "your security questions correctly.\n")
                return self.callback()

    @staticmethod
    def verify_security_answers(row):
        """
        Prompts the user to answer their security questions.
        - If the answers are correct, return True.
        - If the answers are incorrect, return False.
        """
        if row[3] == "" or row[3] is None:
            print(f"{Fore.RED}\nYou have not set any "
                  "security questions.\n")
            return False

        security_questions_and_answers = re.sub(
            r"(?<![\w\\])'|'(?![\w\\])", "\"", row[3])
        if isinstance(security_questions_and_answers, str):
            security_questions_and_answers = json.loads(
                security_questions_and_answers)
        for question_and_answer in security_questions_and_answers:
            question = question_and_answer[0]
            answer = question_and_answer[1]
            user_answer = input(f"\n{question}\n")
            if user_answer.lower() != answer.lower():
                print(f"{Fore.RED}\nIncorrect answer.\n")
                return False
        return True
