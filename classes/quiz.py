import re
import json
from classes.worksheet import Worksheet


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

        compatibility_answers = self.user.compatibility_answers if self.user.compatibility_answers is not None else []

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

        compatibility_questions = [
            ["Are you more of an introvert or extrovert?",
                ["Introvert", "Extrovert"]],
            ["Do you prefer cities or countryside?", ["Cities", "Countryside"]],
            ["Are you more of a planner or spontaneous?",
             ["Planner", "Spontaneous"]],
            ["Are you a dog person, a cat person, both or neither?",
             ["Dog", "Cat", "Dogs and Cats", "Neither"]],
            ["Do you prefer sweet or savory food?", ["Sweet", "Savory"]],
            ["Do you prefer books, films, or both equally?", [
                "Books", "Films", "Books and Films equally"]],
            ["Do you prefer active getaways, relaxed getaways, both or neither?", [
                "Active", "Relaxed", "Both", "I don't like getaways"]],
            ["Are you more logical or emotional?", ["Logical", "Emotional"]],
            ["Do you prefer eating out, cooking at home, or either?",
             ["Eating out", "Cooking at home", "Either"]],
            ["Do you prefer traveling or staying home?",
             ["Traveling", "Staying home"]]
        ]

        quiz_option = input(
            "Would you like to view your answers or take the quiz?\n1. View answers\t   2. Take quiz\t  3. Return to main menu\n")
        if quiz_option == "1":
            print("\nView answers:")

            if len(compatibility_answers) == 0:
                print("\nYou have not yet completed the compatibility quiz\n")
                return self.present_compatibility_quiz()

            for question, answer in zip(
                    compatibility_questions, compatibility_answers):
                print(f"\n{question[0]}\n")
                print(f"{answer}\n")
            return self.present_compatibility_quiz()

        if quiz_option == "2":
            print("\nTake quiz:\n")
            compatibility_answers = []
            for question in compatibility_questions:
                print(f"\n{question[0]}\n")
                for index, option in enumerate(question[1]):
                    print(f"{index+1}. {option}")
                valid_answer = False
                while valid_answer is False:
                    answer = input("Please enter your answer:\n")
                    try:
                        answer = int(answer)
                        if answer in range(1, len(question[1]) + 1):
                            valid_answer = True
                            chosen_answer = question[1][answer - 1]
                        else:
                            print(
                                f"\nThe number between 1 and {len(question[1])}")
                    except ValueError:
                        print("\nPlease enter a valid number\n")
                        continue

                compatibility_answers.append(chosen_answer)

            self.user.compatibility_answers = str(compatibility_answers)

            worksheet = Worksheet()
            worksheet.update_cell(self.row_num, 12,
                                  str(compatibility_answers))

            print("\nQuiz complete and answers updated!\n")

            return self.present_compatibility_quiz()

        if quiz_option == "3":
            print("\nReturn to main menu\n")
            return self.callback(self.user)

        print("\nPlease enter either '1', '2' or '3'\n")
        return self.present_compatibility_quiz()
