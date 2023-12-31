"""
The Quiz class is responsible for handling the compatibility quiz.
- Presents the user with 10 questions.
- User answers the questions.
- Answers are stored in a list and returned.
- Allows the user to view their answers.
"""
import re
import json
from colorama import Fore, init
from classes.worksheet import Worksheet
from classes.mixins import ClearTerminalMixin


init(autoreset=True)

COMPATIBILITY_QUESTIONS = [
    ["Are you more of an introvert or extrovert?",
     ["Introvert", "Extrovert"]],
    ["Do you prefer cities or countryside?",
     ["Cities", "Countryside"]],
    ["Are you more of a planner or spontaneous?",
     ["Planner", "Spontaneous"]],
    ["Are you a dog person, a cat person, both or neither?",
     ["Dog", "Cat", "Dogs and Cats", "Neither"]],
    ["Do you prefer sweet or savory food?", ["Sweet", "Savory"]],
    ["Do you prefer books, films, or both equally?", [
        "Books", "Films", "Books and Films equally"]],
    ["Do you prefer active getaways, relaxed getaways,"
     " both or neither?",
     ["Active", "Relaxed", "Both", "I don't like getaways"]],
    ["Are you more logical or emotional?", ["Logical", "Emotional"]],
    ["Do you prefer eating out, cooking at home, or either?",
     ["Eating out", "Cooking at home", "Either"]],
    ["Do you prefer traveling or staying home?",
     ["Traveling", "Staying home"]]
]


class Quiz():
    """
    Presents the user with the compatibility quiz
    answers and the quiz itself.
    """

    def __init__(self, user, callback):
        self.user = user
        self.row_num = user.row_num
        self.callback = callback

    def present_compatibility_quiz(self):
        """
        Runs the compatibility quiz.
        - Presents the user with 10 questions.
        - User answers the questions.
        - Answers are stored in a list and returned.
        """

        print(f"{Fore.YELLOW}Compatibility Quiz\n")

        compatibility_answers = (self.user.compatibility_answers
                                 if self.user.compatibility_answers is not
                                 None else [])

        if isinstance(compatibility_answers, str) and len(
                compatibility_answers) > 0:
            # regex to replace single quotes with double quotes
            compatibility_answers = re.sub(
                r"(?<![\w\\])'|'(?![\w\\])", "\"", compatibility_answers)
            compatibility_answers = json.loads(compatibility_answers)
        elif isinstance(compatibility_answers, list):
            pass
        else:
            compatibility_answers = []

        quiz_option = input("\nWould you like to view your "
                            "answers or take the quiz?\n"
                            "\n1. View answers     2. Take "
                            "quiz     3. Return to main menu\n")

        if quiz_option == "1":
            ClearTerminalMixin.clear_terminal()
            print(f"{Fore.YELLOW}\nView answers\n")

            if len(compatibility_answers) == 0:
                print(
                    f"\n{Fore.RED}You have not yet completed "
                    "the compatibility quiz.\n")

                ClearTerminalMixin.clear_terminal(2)
                return self.present_compatibility_quiz()

            for question, answer in zip(
                    COMPATIBILITY_QUESTIONS, compatibility_answers):
                print(f"\n{question[0]}\n")
                print(f"{answer}\n")
            return self.present_compatibility_quiz()

        if quiz_option == "2":
            ClearTerminalMixin.clear_terminal()
            print(f"{Fore.YELLOW}\nQuiz")
            compatibility_answers = []
            for question in COMPATIBILITY_QUESTIONS:
                print(f"\n{question[0]}\n")
                for index, option in enumerate(question[1]):
                    print(f"{index+1}. {option}")
                valid_answer = False
                while valid_answer is False:
                    answer = input(
                        "\nPlease enter your answer or press 'q' to cancel:\n")
                    try:
                        if answer == "q":
                            print(
                                f"{Fore.RED}\nQuiz cancelled - answers not saved.")
                            print("\nReturning to compatibility quiz menu...\n")
                            ClearTerminalMixin.clear_terminal(2)
                            return self.present_compatibility_quiz()
                        answer = int(answer)
                        if answer in range(1, len(question[1]) + 1):
                            valid_answer = True
                            chosen_answer = question[1][answer - 1]
                        else:
                            print(f"{Fore.RED}\nChoose a number between "
                                  f"1 and {len(question[1])},"
                                  f" or press 'q' to cancel.\n")

                    except ValueError:
                        continue

                compatibility_answers.append(chosen_answer)

            self.user.compatibility_answers = str(compatibility_answers)

            worksheet = Worksheet()
            worksheet.update_cell(self.row_num, 12,
                                  str(compatibility_answers))

            print(f"{Fore.GREEN}\nQuiz complete and answers updated!\n")
            ClearTerminalMixin.clear_terminal(2)

            return self.present_compatibility_quiz()

        if quiz_option == "3":
            print("\nReturning to main menu...\n")
            ClearTerminalMixin.clear_terminal(1)
            return self.callback(self.user)

        print("\nPlease enter either '1', '2' or '3'\n")
        return self.present_compatibility_quiz()
