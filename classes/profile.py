"""
The Profile class is responsible for handling the profile details of the user,
some of which are added at the account creation step, and which can be edited
later on.
"""

import json
from colorama import Fore, init
from classes.authenticaton import Authentication
from classes.worksheet import Worksheet
from classes.mixins import ClearTerminalMixin

init(autoreset=True)


class Profile():
    """
    This class handles the profile details of the user, some of
    which are added at the account creation step, and which can
    be edited later on.
    """

    def __init__(self, user, callback):
        self.user = user
        self.callback = callback

    @staticmethod
    def prompt_for_age():
        """
        Prompt the user for their age.\n
        - If the user is under 18, let them know they can't use the app.\n
        - If the user is 18 or over, return their age.
        """
        age = input("\nPlease enter your age:\n")
        if not age.isdigit():
            print(f"{Fore.RED}\nYou must enter a number between 18 and 100.\n")
            return Profile.prompt_for_age()

        age = int(age)
        if age < 18:
            print(f"""{Fore.RED}
Sorry! You must be at least 18 years old to use Console Connections.
""")
            return Profile.prompt_for_age()

        if age >= 100:
            print("""
While we admire your vitality, users must between the ages of 18 and 100
""")
            return Profile.prompt_for_age()

        return age

    @staticmethod
    def prompt_for_gender():
        """
        Gets the user's gender.
        """
        gender_input = input("""
Please input the gender you identify as:

1. Male     2. Female     3. Non-binary
""").lower()

        if gender_input == "1" or gender_input == "male":
            gender = "Male"
        elif gender_input == "2" or gender_input == "female":
            gender = "Female"
        elif gender_input == "3" or gender_input == "non-binary":
            gender = "Non-binary"
        else:
            print(f"""{Fore.RED}
Please enter one of the above genders using 1, 2, or 3.
""")
            return Profile.prompt_for_gender()

        return gender

    @staticmethod
    def set_age_range_seeking():
        """
        Sets the minimum and maximum age that the user wants to match with.
        Minimum must be 18 and maximum is 100.
        """
        min_age = input("""
What is the minimum age you want to match with? The age must be 18 or over.
""")

        if not min_age.isdigit():
            print(f"{Fore.RED}\nPlease enter a number between 18 and 100\n")
            return Profile.set_age_range_seeking()

        if int(min_age) < 18:
            print(f"""{Fore.RED}
The minimum age must be 18 or over.
""")
            return Profile.set_age_range_seeking()

        max_age = input("""
What is the maximum age you want to match with? The age must be 18 or over.
""")

        if not max_age.isdigit():
            print(f"{Fore.RED}\nPlease enter a number between 18 and 100\n")
            return Profile.set_age_range_seeking()

        if int(max_age) < int(min_age):
            ClearTerminalMixin.clear_terminal()
            print(f"""{Fore.RED}
The maximum age must be greater than or equal to the minimum age.
""")
            return Profile.set_age_range_seeking()

        if int(max_age) > 100:
            print(f"""{Fore.RED}
The maximum age must be 100 or under.
""")
            return Profile.set_age_range_seeking()

        if int(max_age) < 18:
            print(f"""{Fore.RED}
The maximum age must be 18 or over.
""")
            return Profile.set_age_range_seeking()

        return [int(min_age), int(max_age)]

    def set_genders_seeking(self, user):
        """
        Lets the user set or update their gender seeking preferences.
        They are able to choose multiple genders if they wish.
        """

        available_genders = ["Male", "Female", "Non-binary"]
        if isinstance(user.genders_seeking, list) is False:
            current_genders = json.loads(
                user.genders_seeking.replace(
                    "'", '"')) if user.genders_seeking else []
        else:
            current_genders = user.genders_seeking

        while True:
            # print out genders already in preferences
            print("\nHere are your currently selected genders:\n")
            for gender in current_genders:
                print(gender)

            action = input("""
Do you want to (a)dd or (r)emove genders or (q)uit?
""").lower()

            if action == 'a' and len(current_genders) < len(available_genders):
                print("\nAvailable genders to add:\n")
                for index, gender in enumerate(
                    [gender for gender in available_genders
                     if gender not in current_genders],
                        start=1):
                    print(f"{index}. {gender}\n")
                add_gender = input(
                    "\nEnter the number of the gender you want to add:\n")
                try:
                    chosen_gender = [
                        gender for gender in available_genders
                        if gender not in current_genders][int(add_gender) - 1]
                    current_genders.append(chosen_gender)
                    print(f"""{Fore.GREEN}
{chosen_gender} has been added to your gender seeking preferences.
""")
                    ClearTerminalMixin.clear_terminal(2)
                except (IndexError, ValueError):
                    print("Invalid choice. Please try again.")

            elif action == 'r' and len(current_genders) > 0:
                print("\nCurrent genders selected:\n")
                for index, gender in enumerate(current_genders, start=1):
                    print(f"{index}. {gender}")
                remove_gender = input(
                    "\nEnter the number of the gender you want to remove:\n")
                try:
                    chosen_gender = current_genders[int(remove_gender) - 1]
                    current_genders.remove(chosen_gender)
                    print(f"""{Fore.GREEN}
{chosen_gender} has been removed from your gender seeking preferences.
""")
                    ClearTerminalMixin.clear_terminal(2)
                except (IndexError, ValueError):
                    print(f"{Fore.RED}Invalid choice. Please try again.")

            elif action == 'q':
                if len(current_genders) == 0:
                    print(f"""{Fore.RED}
You need to add at least one gender to your preferences.
""")
                else:
                    return current_genders
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.")

    def present_edit_profile(self):
        """
        Allows the user to update their password, security questions, bio,
        the ages they're interested in and the gender(s) they're interested in.
        """

        finsihed_editing = False

        while finsihed_editing is False:
            print("{Fore.YELLOW}Edit profile\n")

            ClearTerminalMixin.clear_terminal()
            print(f"""
Here is your current profile information:

{Fore.RED}Uneditable:{Fore.WHITE}
Usercode: {self.user.usercode}
Alias: {self.user.alias}

{Fore.GREEN}Editable:{Fore.WHITE}
    1. Password: {self.user.password}
    2. Security questions: {self.user.security_questions_and_answers}
    3. Bio: {self.user.bio}
    4. Age range to match with: {self.user.age_range_seeking}
    5. Genders to match with: {self.user.genders_seeking}
    6. Save and exit
""")

            edit_profile_option = input("""
Please enter the number of the field you would like to edit,
or enter '6' to save and exit:
""")
            if edit_profile_option == "1":
                authentication = Authentication("", self.present_edit_profile)
                self.user.password = authentication.prompt_for_password(
                    "updating")
            elif edit_profile_option == "2":
                auth_check = Authentication.prompt_for_security_questions()
                self.user.security_questions_and_answers = auth_check
            elif edit_profile_option == "3":
                self.user.bio = input("\nPlease enter your bio:\n")
            elif edit_profile_option == "4":
                self.user.age_range_seeking = self.set_age_range_seeking()
            elif edit_profile_option == "5":
                self.user.genders_seeking = self.set_genders_seeking(
                    self.user)
            elif edit_profile_option == "6":
                print(f"{Fore.YELLOW}\nSaving changes...\n")

                worksheet = Worksheet()
                worksheet.update_row(self.user.row_num, [
                    self.user.usercode,
                    self.user.password,
                    self.user.alias,
                    str(self.user.security_questions_and_answers),
                    self.user.age,
                    self.user.gender,
                    self.user.bio,
                    str(self.user.genders_seeking),
                    str(self.user.age_range_seeking),
                    str(self.user.messages),
                    str(self.user.allow_contact_list),
                    str(self.user.compatibility_answers),
                    self.user.row_num
                ])

                print(f"{Fore.GREEN}\nProfile saved!\n")
                ClearTerminalMixin.clear_terminal(2)
                return self.callback(self.user)
            else:
                print(f"{Fore.RED}\nPlease enter a number between 1 and 6")
