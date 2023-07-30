import re
import os
import json
import random
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

CONSOLE_CONNECTIONS_HEADING = """     ,gggg,                                                                     ,gggg,                                                                                                          
   ,88YYYY8b,                                               ,dPYb,            ,88YYYY8b,                                                          I8                                            
  d8"     `Y8                                               IP'`Yb           d8"     `Y8                                                          I8                                            
 d8'   8b  d8                                               I8  8I          d8'   8b  d8                                                       88888888 gg                                      
,8I    "Y88P'                                               I8  8'         ,8I    "Y88P'                                                          I8    ""                                      
I8'            ,ggggg,    ,ggg,,ggg,     ,g,      ,ggggg,   I8 dP  ,ggg,   I8'            ,ggggg,    ,ggg,,ggg,   ,ggg,,ggg,   ,ggg,     ,gggg,   I8    gg     ,ggggg,    ,ggg,,ggg,     ,g,    
d8            dP"  "Y8ggg,8" "8P" "8,   ,8'8,    dP"  "Y8gggI8dP  i8" "8i  d8            dP"  "Y8ggg,8" "8P" "8, ,8" "8P" "8, i8" "8i   dP"  "Yb  I8    88    dP"  "Y8ggg,8" "8P" "8,   ,8'8,   
Y8,          i8'    ,8I  I8   8I   8I  ,8'  Yb  i8'    ,8I  I8P   I8, ,8I  Y8,          i8'    ,8I  I8   8I   8I I8   8I   8I I8, ,8I  i8'       ,I8,   88   i8'    ,8I  I8   8I   8I  ,8'  Yb  
`Yba,,_____,,d8,   ,d8' ,dP   8I   Yb,,8'_   8),d8,   ,d8' ,d8b,_ `YbadP'  `Yba,,_____,,d8,   ,d8' ,dP   8I   Yb,dP   8I   Yb,`YbadP' ,d8,_    _,d88b,_,88,_,d8,   ,d8' ,dP   8I   Yb,,8'_   8) 
  `"Y8888888P"Y8888P"   8P'   8I   `Y8P' "YY8P8P"Y8888P"   8P'"Y8888P"Y888   `"Y8888888P"Y8888P"   8P'   8I   `Y8P'   8I   `Y888P"Y888P""Y8888PP8P""Y88P""Y8P"Y8888P"   8P'   8I   `Y8P' "YY8P8P                                                                                                                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                """


APP_SUBHEADING = """\t\t\t\t\t\t\t\t\t\t\u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764\n\n\t\t\t\t\t\t\t\t\t\tThere's no cover to judge here!\n\n\t\t\t\t\t\t\t\t\t\t\u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764\n"""


class User:
    """
    A class to represent a user.\n
    """

    def __init__(self, usercode, password, alias, security_questions_and_answers, age, gender, bio='', genders_seeking=None, age_range_seeking=None, messages=None, allow_contact_list=None, compatibility_answers=None, row_num=None):
        self.usercode = usercode
        self.password = password
        self.alias = alias
        self.security_questions_and_answers = security_questions_and_answers
        self.age = age
        self.gender = gender
        self.bio = bio if bio is not None else "No bio yet"
        self.genders_seeking = genders_seeking if genders_seeking is not None else []
        self.age_range_seeking = age_range_seeking if age_range_seeking is not None else [
            18, 100]
        self.messages = messages if messages is not None else []
        self.allow_contact_list = allow_contact_list if allow_contact_list is not None else []
        self.compatibility_answers = compatibility_answers if compatibility_answers is not None else []
        self.row_num = row_num

    def set_age_range_seeking(self):
        """
        Sets the minimum and maximum age that the user wants to match with.
        Minimum must be 18 and maximum is 100.
        """
        min_age = input(
            "\nWhat is the minimum age you would like to match with? The age must be 18 or over.\n")
        if not min_age.isdigit():
            print("\nPlease enter a number between 18 and 100\n")
            return self.set_age_range_seeking()

        max_age = input(
            "\nWhat is the maximum age you would like to match with? The age must be 18 or over.\n")
        if not max_age.isdigit():
            print("\nPlease enter a number between 18 and 100\n")
            return self.set_age_range_seeking()

        return [int(min_age), int(max_age)]

    def set_genders_seeking(self):
        # TODO: fix this function as it currently outputs each letter of each
        # gender instead of just the gender.
        """
        Lets the user set or update their gender seeking preferences.
        They are able to choose multiple genders if they wish.
        """
        current_genders = self.genders_seeking
        for index, gender in enumerate(current_genders):
            print(f"{index}. {gender}")

        available_genders = ["Male", "Female", "Non-binary"]

        genders_to_add = [
            gender for gender in available_genders if gender not in current_genders]

        if len(genders_to_add) == 0:
            print("You have already selected all available genders.")
        else:
            print("Available genders to add:")
            for index, gender in enumerate(genders_to_add):
                print(f"{index}. {gender}")

        if len(current_genders) == 0:
            print("You have not selected any genders.")
        else:
            print("Current genders selected:")
            for index, gender in enumerate(current_genders):
                print(f"{index}. {gender}")

        while True:
            action = input(
                "Enter the number of the gender you want to add, or '-' followed by the number of the gender you want to remove, or 'q' to quit: ")
            if action == "q":
                break

            try:
                if action.startswith("-"):
                    gender_index = int(action[1:])
                    if gender_index < 0 or gender_index >= len(current_genders):
                        print("Invalid gender index. Please try again.")
                        continue

                    gender_to_remove = current_genders[gender_index]
                    self.genders_seeking.remove(gender_to_remove)
                    print(
                        f"{gender_to_remove} has been removed from your gender seeking preferences.")
                    break

                else:
                    gender_index = int(action)
                    if gender_index < 0 or gender_index >= len(genders_to_add):
                        print("Invalid gender index. Please try again.")
                        continue

                    gender_to_add = genders_to_add[gender_index]
                    if gender_to_add in current_genders:
                        print(
                            "You have already selected this gender. Please choose a different one.")
                        continue

                    self.genders_seeking.append(gender_to_add)
                    print(
                        f"{gender_to_add} has been added to your gender seeking preferences.")
                    break

            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")

        return genders_to_add

    def present_compatibility_quiz(self, worksheet_selected):
        """
        Runs the compatibility quiz.\n
        - Presents the user with 10 questions.\n
        - User answers the questions.\n
        - Answers are stored in a list and returned.
        """

        # regex to replace single quotes with double quotes
        compatibility_answers = re.sub(
            r"(?<![\w\\])'|'(?![\w\\])", "\"", self.compatibility_answers)
        print(compatibility_answers)
        # convert string to list
        compatibility_answers = json.loads(compatibility_answers)

        compatibility_questions = [
            ["Are you more of an introvert or extrovert?",
                ["Introvert", "Extrovert"]],
            ["Do you prefer cities or countryside?", ["Cities", "Countryside"]],
            ["Do you prefer a planner or spontaneous?",
                ["Planner", "Spontaneous"]],
            ["Are you a dog person or a cat person?",
                ["Dog", "Cat", "Both", "Neither"]],
            ["Do you prefer sweet or savory food?", ["Sweet", "Savory"]],
            ["Do you prefer books or films?", ["Books", "Films", "Both"]],
            ["Do you prefer active or relaxed getaways?", [
                "Active", "Relaxed", "Both", "I don't like getaways"]],
            ["Are you more logical or emotional?", ["Logical", "Emotional"]],
            ["Do you prefer eating out or cooking at home?",
                ["Eating out", "Cooking at home", "Both"]],
            ["Do you prefer traveling or staying home?",
                ["Traveling", "Staying home"]]
        ]

        quiz_option = input(
            "Would you like to view your answers or take the quiz?\n 1. View answers\t 2. Take quiz\n 3. Return to main menu\n")
        if quiz_option == "1":
            print("\nView answers:")

            if len(compatibility_answers) == 0:
                print("\nYou have not yet completed the compatibility quiz\n")
                return self.present_compatibility_quiz(worksheet_selected)

            for question, answer in zip(compatibility_questions, compatibility_answers):
                print(f"\n{question[0]}\n")
                print(f"{answer}\n")
            return self.present_compatibility_quiz(worksheet_selected)

        elif quiz_option == "2":
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
                        if answer in range(1, len(question[1])+1):
                            valid_answer = True
                        else:
                            print(
                                f"\nThe number between 1 and {len(question[1])}")
                    except ValueError:
                        print("\nPlease enter a valid number\n")
                        continue

                compatibility_answers.append(option)

            SHEET.worksheet(worksheet_selected).update_cell(
                self.row_num, 12, str(compatibility_answers))

            print("\nQuiz complete and answers updated!\n")

            return self.present_compatibility_quiz(worksheet_selected)
        elif quiz_option == "3":
            print("\nReturn to main menu\n")
            return present_main_menu(self, worksheet_selected)
        else:
            print("\nPlease enter either '1', '2' or '3'\n")
            return self.present_compatibility_quiz(worksheet_selected)

    def present_edit_profile(self, worksheet_selected):
        """
        Allows the user to update their password, security questions, bio,
        the ages they're interested in and the gender(s) they're interested in.
        """
        print("\nEdit profile:\n")
        print("Here is your current profile information:\n")

        print("Uneditable:\n")
        print(f"Usercode: {self.usercode}\n")
        print(f"Alias: {self.alias}\n")

        print("Editable:\n")
        print(f"1. Password: {self.password}\n")
        print(
            f"2. Security questions: {self.security_questions_and_answers}\n")
        print(f"3. Bio: {self.bio}\n")
        print(f"4. Age range to match with: {self.age_range_seeking}\n")
        print(f"5. Genders to match with {self.genders_seeking}\n")
        print("6. Save and exit\n")

        finsihed_editing = False
        while finsihed_editing is False:
            edit_profile_option = input(
                "Please enter the number of the field you would like to edit:\n")
            if edit_profile_option == "1":
                self.password = prompt_for_password("updating")
            elif edit_profile_option == "2":
                self.security_questions_and_answers = prompt_for_security_questions_and_answers()
            elif edit_profile_option == "3":
                self.bio = input("\nPlease enter your bio:\n")
            elif edit_profile_option == "4":
                self.age_range_seeking = self.set_age_range_seeking()
            elif edit_profile_option == "5":
                self.genders_seeking = self.set_genders_seeking()
            elif edit_profile_option == "6":
                print("\nSaving changes...\n")
                # update google sheet with new profile information
                SHEET.worksheet(worksheet_selected).update_cell(
                    self.row_num, 2, self.password)
                SHEET.worksheet(worksheet_selected).update_cell(
                    self.row_num, 4, str(self.security_questions_and_answers))
                SHEET.worksheet(worksheet_selected).update_cell(
                    self.row_num, 7, self.bio)
                SHEET.worksheet(worksheet_selected).update_cell(
                    self.row_num, 8, str(self.age_range_seeking))
                SHEET.worksheet(worksheet_selected).update_cell(
                    self.row_num, 9, str(self.genders_seeking))

                print("\nProfile saved!\n")
                return present_main_menu(self, worksheet_selected)
            else:
                print("\nPlease enter a number between 1 and 6")


def clear_terminal():
    """
    Clears the terminal window.
    """
    # https://www.delftstack.com/howto/python/python-clear-console/
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def establish_user_data():
    """
    Establish if the user is a real user or a test user.\n
    - If a test user, pull data from the test user worksheet.\n
    - If a real user, pull data from the real user worksheet.
    """

    while True:
        user_type = input(
            "\nAre you just testing the app or here to find a connection?\n 1. Tester\t 2. Real User\n")

        if user_type == "1":
            print("\nWelcome to the test version of the app - feel free to play\naround and make some connections with imaginary people.\n")
            # return data from test user worksheet (also breaks the loop)
            return [SHEET.worksheet('test_users').get_all_values(), "test_users"]
        elif user_type == "2":
            worksheet_selected = "real_users"
            print(
                "\nWelcome to the real version of the app - let's make some connections!\n")
            # return data from real user worksheet (also breaks the loop)
            return [SHEET.worksheet('real_users').get_all_values(), "real_users"]
        else:
            print("Please enter either '1' or '2' to continue\n")


def validate_password(password):
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


def prompt_for_password(new_or_existing_user, row=None):
    """
    Prompt the user for a password and validate it.\n
    - If the user is a new user, prompt them to create a password.\n
    - If the user is an existing user, prompt them to enter their password.\n
    - If the password is valid, return the password.\n
    - If the password is invalid, prompt the user to try again.
    """
    password_valid = False
    while password_valid is False:
        password_input = input("Please enter your password:\n")
        password_valid = validate_password(password_input)
        if password_valid is True:
            if new_or_existing_user == "new":
                return password_input
            elif new_or_existing_user == "existing":
                if password_input == row[1]:
                    print("\nPassword correct\n")
                    return password_input
                else:
                    print("\nPassword incorrect\n")
                    password_valid = False
            elif new_or_existing_user == "updating":
                return password_input


def user_login(data, worksheet_selected):
    """
    Checks if the user exists on the Google Sheet.\n
    - If the user exists, prompt them for password.\n
    - If the user doesn't exist, let them know and ask if they want to signup.\n
    """
    user_exists = False
    while user_exists is False:
        usercode_input = int(input("\nPlease enter your usercode:\n"))
        # checks the first column of the data for the usercode
        for index, row in enumerate(data):
            if row[0] == str(usercode_input):
                user_exists = True
                # prompt for password
                password = prompt_for_password("existing", row)
                if password is not None:
                    print("\nLogin successful\n")
                    return User(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], index + 1)
                break
        else:
            print("\nUsercode not found.\n")


def generate_random_usercode(data):
    """
    - Generates a new 6-digit usercode for the user.\n
    - Checks if the usercode already exists in the database.\n
    - If the usercode exists, generate a new one.\n
    """
    usercode = random.randint(100000, 999999)
    # check if the usercode already exists in the database
    for row in data:
        if row[0] == str(usercode):
            # if the usercode exists, generate a new one
            generate_random_usercode(data)
    return usercode


def create_and_validate_alias(data):
    """
    Checks the user's alias against the Google Sheet.\n
    - Make sure the alias is no more than 16 characters.\n
    - If the alias exists, prompt the user to come up with a new alias.\n
    - If the alias doesn't exist, return the alias.
    """
    alias = input("\nYou will also need to create an alias, which may be used for in-app communication.\nThe alias must be unique and it is recommended that it does not easily identify you (for security reasons).\nPlease enter your alias now:\n")
    # check if the alias is greater than 3 but fewer than 16 characters
    while len(alias) < 3 or len(alias) > 16:
        alias = input(
            "\nAlias must be greater than 3 but fewer than 16 characters. Please try again:\n")

    # check if the alias already exists in the database
    for row in data:
        if row[2] == alias:
            # if the alias exists, prompt the user to come up with a new alias
            print("\nAlias already exists.\n")
            return create_and_validate_alias(data)
    return alias


def prompt_for_security_questions_and_answers():
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
        if not security_question_input.isdigit() or int(security_question_input) < 1 or int(security_question_input) > 10:
            print("\nPlease enter a number between 1 and 10\n")
            continue
        security_question_input = int(security_question_input)
        security_question = security_question_list[security_question_input-1]
        security_answer = input(
            f"\nPlease enter your answer to the question '{security_question}':\n")
        security_questions_and_answers.append(
            [security_question, security_answer])
        security_question_list.pop(security_question_input-1)
        print("\nThank you. Please choose another question from the list below:\n")
        for index, question in enumerate(security_question_list):
            print(f"{index+1}. {question}")

    return security_questions_and_answers


def prompt_for_age():
    """
    Prompt the user for their age.\n
    - If the user is under 18, let them know they can't use the app.\n
    - If the user is 18 or over, return their age.
    """
    age = input("\nPlease enter your age:\n")
    if not age.isdigit():
        print("\nYou must enter a number between 18 and 100.\n")
        return prompt_for_age()

    age = int(age)
    if age < 18:
        print("\nSorry! You must be at least 18 years old to use Console Connections.\n")
        return prompt_for_age()

    if age >= 100:
        print(
            "\nWhile we admire your vitality, users must between the ages of 18 and 100.\n")
        return prompt_for_age()

    return age


def prompt_for_gender():
    """
    Gets the user's gender.
    """
    gender_input = input(
        "\nPlease input the gender you identify as: \n\n 1. Male\t 2. Female\t 3. Non-binary\n").lower()

    if gender_input == "1" or gender_input == "male":
        gender = "Male"
    elif gender_input == "2" or gender_input == "female":
        gender = "Female"
    elif gender_input == "3" or gender_input == "non-binary":
        gender = "Non-binary"
    else:
        print("\nPlease enter one of the above genders using 1, 2, or 3.\n")
        return prompt_for_gender()

    return gender


def user_signup(data, worksheet_selected):
    """
    Runs generate usercode, password, alias and security question functions.\n
    - Adds the user to the Google sheet.
    """
    usercode = generate_random_usercode(data)
    print(
        f"If you complete the signup process, your usercode will be {usercode}. Please keep this safe as you will need it to login.\n")
    password = prompt_for_password("new")
    alias = create_and_validate_alias(data)
    clear_terminal()
    print("\Great! We've got your username, password and alias!\n\n")
    security_questions_and_answers = prompt_for_security_questions_and_answers()

    clear_terminal()
    print("\nSecurity questions added!\n")
    age = prompt_for_age()
    gender = prompt_for_gender()

    row_num = len(data) + 1
    # create user object
    user = User(usercode, password, alias,
                security_questions_and_answers, age, gender, None, None, None, None, None, None, row_num)

    # add user to Google Sheet
    SHEET.worksheet(worksheet_selected).append_row([user.usercode, user.password, user.alias, str(
        user.security_questions_and_answers), user.age, user.gender, None, None, None, None, None, None, row_num])

    print(f"\nSignup successful! Remember, your usercode is {usercode}.\n")
    return user


def present_login_signup_step(data, worksheet_selected):
    """
    Provide the user with the option to login or signup.\n
    - If login, check if the user exists in the database and run the login function (if they exist)\n
    - If signup, check if the user exists in the database and run the signup function (if they don't exist).
    """
    while True:
        login_signup = input(
            "Would you like to login or signup? Please enter 1 or 2.\n 1. Login\t 2. Signup\n")

        if login_signup == "1":
            clear_terminal()
            print("\nLogin\n")
            # return data from login function (also breaks the loop)
            return user_login(data, worksheet_selected)
        elif login_signup == "2":
            clear_terminal()
            print("\nSignup\n")
            # return data from signup function (also breaks the loop)
            return user_signup(data, worksheet_selected)
        else:
            print("\nPlease enter either '1' to Login or '2' to Signup\n")


def present_main_menu(user, worksheet_selected):
    """
    Present the user with the main menu options.\n
    - If the user selects '1', run the compatibility quiz.\n
    - If the user selects '2', run the edit profile function.\n
    - If the user selects '3', run the view messages function.\n
    - If the user selects '4', run the logout function.\n
    """
    while True:
        main_menu_input = input(
            "\nWhat would you like to do?\n 1. Compatibility quiz\t 2. Edit profile\t 3. View messages\t 4. Logout\n")

        if main_menu_input == "1":
            print("\nCompatibility quiz\n")
            # return data from compatibility quiz function
            return user.present_compatibility_quiz(worksheet_selected)
        elif main_menu_input == "2":
            print("\nEdit profile\n")
            # return data from edit profile function
            return user.present_edit_profile(worksheet_selected)
        # elif main_menu_input == "3":
        #     print("\nView messages\n")
        #     # return data from view messages function
        #     return present_view_messages(user, worksheet_selected)
        # elif main_menu_input == "4":
        #     print("\nLogout\n")
        #     # return data from logout function
        #     return present_logout(user, worksheet_selected)
        else:
            print("\nPlease enter a number between 1 and 4\n")


def main():
    """
    Run all program functions
    """
    # clear_terminal()
    # print(
    #     f"\t\t\t\t\t\t\t\t\t\t\tWelcome to\n\n{CONSOLE_CONNECTIONS_HEADING}\n{APP_SUBHEADING}")
    [user_data, worksheet_selected] = establish_user_data()
    user = present_login_signup_step(user_data, worksheet_selected)
    present_main_menu(user, worksheet_selected)


main()
