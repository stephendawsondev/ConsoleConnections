import re
import time
import json
from classes.worksheet import Worksheet
from classes.message import Message
from classes.mixins import ClearTerminalMixin


class Matcher():
    """
    Carries out the match calculations and displays the results.
    """

    def __init__(self, user, callback):
        self.user = user
        self.callback = callback

    def view_top_matches(self):
        """
        Displays the matches with the highest compatibility score.\n
        """
        return self.filter_users()

    def filter_users(self):
        """
        Filters out users who don't match the user's preferences.
        - Filters out users who are not the right age.
        - Filters out users whose age range does not include the user's age.
        - Filters out users who do not match the gender the user seeks.
        - Filters out users whose gender seeking preference does not include the user's.
        """
        # get all users from the Google Sheet
        worksheet = Worksheet()
        all_potential_matches = worksheet.get_all_values()

        # remove the first row (the headings)
        all_potential_matches.pop(0)
        # remove user from the list
        all_potential_matches.pop(self.user.row_num - 2)

        potential_matches = [
            potential_match for potential_match in all_potential_matches if potential_match[5] in self.user.genders_seeking]

        # filter out users whose gender preferences don't match the user's
        # gender
        potential_matches = [
            potential_match for potential_match in potential_matches if self.user.gender in potential_match[7]]

        if self.user.age_range_seeking == '':
            self.user.age_range_seeking = [18, 100]
        elif isinstance(self.user.age_range_seeking, list):
            age_range_seeking = self.user.age_range_seeking
        else:
            # filter out users who are not the right age
            age_range_seeking = json.loads(self.user.age_range_seeking)

        [min_age, max_age] = [int(age) for age in age_range_seeking]

        potential_matches = [
            potential_match for potential_match in potential_matches if int(
                potential_match[4]) >= int(min_age) and int(
                potential_match[4]) <= int(max_age)]

        # filter out users whose age range does not include the user's age
        for potential_match in potential_matches:
            try:
                if potential_match[8] == '':
                    potential_match[8] = [18, 100]
                elif isinstance(potential_match[8], list):
                    pass
                else:
                    # filter out users who are not the right age
                    potential_match[8] = json.loads(potential_match[8])
            except ValueError:
                potential_matches.remove(potential_match)
                continue

        potential_matches = [
            potential_match for potential_match in potential_matches if int(
                self.user.age) >= int(
                potential_match[8][0]) and int(
                self.user.age) <= int(
                    potential_match[8][1])]

        # run the compatibility calculations
        self.run_compatibilty_calculations(
            potential_matches, self.user)

        return self.callback(self.user)

    def run_compatibilty_calculations(self, potential_matches, user):
        """
        Runs the compatibility calculations.\n
        - Calculates the percentage match based on each users answers.\n
        - Returns a list of potential matches sorted by percentage of questions in common.
        """

        compatibility_scores = {
            "Introvert": {
                "Introvert": 10,
                "Extrovert": 0,
            },
            "Extrovert": {
                "Introvert": 0,
                "Extrovert": 10,
            },
            "Cities": {
                "Cities": 10,
                "Countryside": 0,
            },
            "Countryside": {
                "Cities": 0,
                "Countryside": 10,
            },
            "Planner": {
                "Planner": 5,
                "Spontaneous": 10,
            },
            "Spontaneous": {
                "Planner": 10,
                "Spontaneous": 5,
            },
            "Dog": {
                "Dog": 10,
                "Cat": 0,
                "Dogs and Cats": 5,
                "Neither": 0,
            },
            "Cat": {
                "Dog": 0,
                "Cat": 10,
                "Dogs and Cats": 5,
                "Neither": 0,
            },
            "Dogs and Cats": {
                "Dog": 5,
                "Cat": 5,
                "Dogs and Cats": 10,
                "Neither": 0,
            },
            "Neither": {
                "Dog": 0,
                "Cat": 0,
                "Dogs and Cats": 0,
                "Neither": 10,
            },
            "Sweet": {
                "Sweet": 10,
                "Savory": 0,
            },
            "Savory": {
                "Sweet": 0,
                "Savory": 10,
            },
            "Books": {
                "Books": 10,
                "Films": 0,
                "Books and Films equally": 5,
            },
            "Films": {
                "Books": 0,
                "Films": 10,
                "Books and Films equally": 5,
            },
            "Books and Films equally": {
                "Books": 5,
                "Films": 5,
                "Books and Films equally": 10,
            },
            "Active": {
                "Active": 10,
                "Relaxed": 0,
                "Both": 5,
                "I don't like getaways": 0,
            },
            "Relaxed": {
                "Active": 0,
                "Relaxed": 10,
                "Both": 5,
                "I don't like getaways": 0,
            },
            "Both": {
                "Active": 5,
                "Relaxed": 5,
                "Both": 10,
                "I don't like getaways": 0,
            },
            "I don't like getaways": {
                "Active": 0,
                "Relaxed": 0,
                "Both": 0,
                "I don't like getaways": 10,
            },
            "Logical": {
                "Logical": 10,
                "Emotional": 0,
            },
            "Emotional": {
                "Logical": 0,
                "Emotional": 10,
            },
            "Eating out": {
                "Eating out": 10,
                "Cooking at home": 0,
                "Either": 5,
            },
            "Cooking at home": {
                "Eating out": 0,
                "Cooking at home": 10,
                "Either": 5,
            },
            "Either": {
                "Eating out": 5,
                "Cooking at home": 5,
                "Either": 10,
            },
            "Traveling": {
                "Traveling": 10,
                "Staying home": 0,
            },
            "Staying home": {
                "Traveling": 0,
                "Staying home": 10,
            }
        }

        # get the user's answers to the compatibility quiz
        compatibility_answers = user.compatibility_answers

        # ensure compatibility_answers is a string
        if isinstance(compatibility_answers, str):
            try:
                compatibility_answers = re.sub(
                    r"(?<![\w\\])'|'(?![\w\\])", "\"", compatibility_answers)
                # convert string to list
                compatibility_answers = json.loads(compatibility_answers)
            except ValueError:
                print(compatibility_answers, type(compatibility_answers))
        elif isinstance(compatibility_answers, list):
            pass
        else:
            print(
                f"Unexpected type {type(compatibility_answers)} for compatibility_answers")

        # create a list of potential matches for those who score over 60%
        matches = []

        for match in potential_matches:
            compatibility_score = 0
            if match[11] == '' or match[11] == '[]':
                continue
            if isinstance(match[11], list):
                pass
            else:
                try:
                    # use regex to make valid json string
                    match[11] = re.sub(
                        r"(?<![\w\\])'|'(?![\w\\])", "\"", match[11])
                    match_compatibility_answers = json.loads(
                        match[11])
                except ValueError:
                    print(match[11], type(match[11]))
                    continue

            # loop through each answer in the user's compatibility answers
            for index, answer in enumerate(compatibility_answers):
                # add the compatibility score to the total
                try:
                    compatibility_score += compatibility_scores[answer][match_compatibility_answers[index]]
                except KeyError:
                    # print detailed error message
                    print(
                        f"\nKeyError: {answer} or {match_compatibility_answers[index]} not found in compatibility_scores\n")
                    continue

            # calculate the percentage match
            percentage_match = round((compatibility_score / 100) * 100)

            # if the percentage match is over 60%, add the user to the list of
            # potential matches
            if percentage_match > 50:
                matches.append([match, percentage_match])

        # sort the list of potential matches by the highest percentage
        # taken from StackOverflow:
        # https://stackoverflow.com/a/65679191/12297743
        sorted_matches = sorted(
            matches, key=lambda x: x[1], reverse=True)

        # return the list of potential matches
        return self.present_matches_options(sorted_matches)

    def present_matches_options(self, matches_list):
        """
        Gives the user the list of matches numbered.
        - If the user selects a number, run the view match method.
        - If the select 'q', return to the main menu.
        """
        if (len(matches_list) == 0):
            print(
                "Sorry, there are no matches that match your preferences. Please try again later.")
            time.sleep(2)
            return self.callback(self.user)
        print("Here are your matches:\n")
        for index, match in enumerate(matches_list, start=1):
            [person, percentage_match] = match
            print(
                f"{index}. {person[2]} ({person[4]}) - {person[5]} - Compatibility: {percentage_match}\nBio: {person[6]}\n")

        while True:
            action = input(
                "\nEnter a match's number to view or 'q' to return to the main menu:\n").lower()
            if action == 'q':
                return self.callback(self.user)
            try:
                match = matches_list[int(action) - 1]
                return self.view_match(match[0], match[1], matches_list)
            except (IndexError, ValueError):
                print("\nInvalid choice. Please try again.\n")
                return self.present_matches_options(matches_list)

    def view_match(self, person, percentage_match, matches_list):
        """
        Displays the match's profile info.
        - If the user allows contact, ask the user is they want to view messages or go back.
        - If the user does not allow contact, ask the user if they want to allow contact.
        - If the user allows contact but the match does not allow contact, inform the user
        that the match does not allow contact yet.
        """
        ClearTerminalMixin.clear_terminal()
        print(
            f"{person[2]} ({person[4]}) - {person[5]} - Compatibility: {percentage_match}\nBio: {person[6]}\n")

        if person[10] == '':
            person[10] = []
        elif isinstance(person[10], list):
            pass
        else:
            try:
                person[10] = json.loads(person[10])
            except ValueError:
                print(person[10], type(person[10]))

        if self.user.allow_contact_list == '':
            self.user.allow_contact_list = []
        elif isinstance(self.user.allow_contact_list, list):
            pass
        else:
            try:
                self.user.allow_contact_list = json.loads(
                    self.user.allow_contact_list)
            except ValueError:
                print(self.user.allow_contact_list,
                      type(self.user.allow_contact_list))

        if int(person[0]) not in self.user.allow_contact_list:
            print("You have not yet allowed this user to contact you.")
            while True:
                action = input(
                    "\nWould you like to allow this user to contact you? (y/n)\n").lower()
                if action == 'y':
                    self.user.allow_contact_list.append(int(person[0]))
                    user_allow_contact_string = str(
                        self.user.allow_contact_list)
                    worksheet = Worksheet()
                    worksheet.update_cell(
                        self.user.row_num, 11, user_allow_contact_string)
                    return self.view_match(
                        person, percentage_match, matches_list)
                if action == 'n':
                    return self.callback(self.user)
                print("\nInvalid choice. Please try again.\n")
        elif int(self.user.usercode) not in person[10]:
            print("This user has not yet allowed you to contact them.")
            time.sleep(2)
            return self.present_matches_options(matches_list)
        else:
            message = Message(self.user, self.callback)
            while True:
                action = input(
                    "\nWould you like to view messages with this user? (y/n)\n").lower()
                if action == 'y':
                    return message.display_messages(person)
                if action == 'n':
                    print("\nReturning to main menu\n")
                    return self.callback(self.user)
                print("\nInvalid choice. Please try again.\n")
