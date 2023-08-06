"""
This module contains the User class, which is used to create
a user object.
"""


class User:
    """
    A class to represent a user. This is created using data from
    the user_access class.
    """

    def __init__(
            self,
            usercode,
            password,
            alias,
            security_questions_and_answers,
            age,
            gender,
            bio='',
            genders_seeking=None,
            age_range_seeking=None,
            messages=None,
            allow_contact_list=None,
            compatibility_answers=None,
            row_num=None):

        self.usercode = usercode
        self.password = password
        self.alias = alias
        self.security_questions_and_answers = security_questions_and_answers
        self.age = age
        self.gender = gender
        self.bio = bio if bio is not None else "No bio yet"
        self.genders_seeking = (genders_seeking if
                                genders_seeking is not None
                                else [])
        self.age_range_seeking = (age_range_seeking if
                                  age_range_seeking is not None
                                  else [18, 100])
        self.messages = messages if messages is not None else []
        self.allow_contact_list = (allow_contact_list if
                                   allow_contact_list is not None
                                   else [])
        self.compatibility_answers = (compatibility_answers if
                                      compatibility_answers is not None
                                      else [])
        self.row_num = row_num
