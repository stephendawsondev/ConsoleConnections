import re
import json
from classes.worksheet import Worksheet


class Matcher():
    """
    Carries out the match calculations and displays the results.
    """

    def __init__(self):
        pass

    def view_top_matches(self, user):
        """
        Displays the matches with the highest compatibility score.\n
        """
        return self.filter_users(user)

    def filter_users(self, user):
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
        # # remove user from the list
        all_potential_matches.pop(user.row_num - 2)

        potential_matches = [
            potential_match for potential_match in all_potential_matches if user[5] in user.genders_seeking]

        # # filter out users whose gender preferences don't match the user's gender
        potential_matches = [
            potential_match for potential_match in potential_matches if user.gender in potential_match[7]]

        # filter out users who are not the right age
        age_range_seeking = json.loads(user.age_range_seeking)

        potential_matches = [
            potential_match for potential_match in potential_matches if int(
                user[4]) >= age_range_seeking[0] and int(
                user[4]) <= age_range_seeking[1]]

        # # filter out users whose age range does not include the user's age
        for potential_match in potential_matches:
            try:
                potential_match[8] = json.loads(potential_match[8])
            except ValueError:
                potential_matches.remove(potential_match)
                continue

        for potential_match in potential_matches:
            if (isinstance(potential_match[8], list) is False):
                potential_matches.remove(potential_match)
                continue

        potential_matches = [
            potential_match for potential_match in potential_matches if int(
                user.age) >= int(
                potential_match[8][0]) and int(
                user.age) <= int(
                    potential_match[8][1])]

        print(
            f"\nThere are {len(potential_matches)} users who match your preferences:\n")

        # run the compatibility calculations
        matches = self.run_compatibilty_calculations(
            potential_matches, user)

        for match in matches:
            print(
                f"{match[0][2]} ({match[0][4]}) - {match[0][5]} - Compatibility: {match[1]}\nBio: {match[0][6]}\n")

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
                print(compatibility_answers, type(compatibility_answers))
                # convert string to list
                compatibility_answers = json.loads(compatibility_answers)
            except ValueError:
                print(compatibility_answers, type(compatibility_answers))
        else:
            print(
                f"Unexpected type {type(compatibility_answers)} for compatibility_answers")

        # create a list of potential matches for those who score over 60%
        matches = []

        # loop through each user in the filtered list
        for match in potential_matches:
            compatibility_score = 0
            try:
                # use regex to make valid json string
                match[11] = re.sub(
                    r"(?<![\w\\])'|'(?![\w\\])", "\"", match[11])
                match_compatibility_answers = json.loads(user[11])
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

            print(compatibility_score)

            # calculate the percentage match
            percentage_match = round((compatibility_score / 100) * 100)

            # if the percentage match is over 60%, add the user to the list of
            # potential matches
            if percentage_match > 60:
                matches.append([match, percentage_match])

        # sort the list of potential matches by the highest percentage
        # taken from StackOverflow:
        # https://stackoverflow.com/a/65679191/12297743
        sorted_matches = sorted(
            matches, key=lambda x: x[1], reverse=True)

        print(sorted_matches)

        # return the list of potential matches
        return sorted_matches
