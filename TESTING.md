# Console Connections -  Testing

## Contents
- [**Test table**](#test-table)
- [**User testing**](#user-testing)
- [**User stories testing**](#user-stories-testing)
    - [**As a first-time user, I want:**](#as-a-first-time-user-i-want)
    - [**As a returning user, I want:**](#as-a-returning-user-i-want)
    - [**As a frequent user, I want:**](#as-a-frequent-user-i-want)
- [**Code testing**](#code-testing)
- [**Bugs and issues table**](#bugs-and-issues-table)
- [**Future features**](#future-features)


### Test table

I used the Code Institute Mock Terminal to test the app. I asked family and friends to test both the test user and real user versions of the app. I also tested the app myself. I used the following test cases:

| Test Case | Test Steps | Expected Result | Actual Result | Pass/Fail |
|-----------|------------|-----------------|---------------|-----------|
| User signup | 1. Select test user option <br>2. Select signup option <br>3. Enter usercode <br>4. Enter password <br>5. Enter security questions <br>6. Enter security answers <br>7. Enter alias | User is signed up and taken to main menu | User is signed up and taken to main menu | Pass |
| User login | 1. Select test user option 2. Select login option 3. Enter usercode 4. Enter password | User is logged in and taken to main menu | User is logged in and taken to main menu | Pass |
| User views matches without completing compatibility quiz | 1.Sign up <br>2. Select view matches option | User is shown a message that they need to complete the compatibility quiz | User is shown a message that they need to complete the compatibility quiz | Pass |
| User views compatibility quiz answers without answer | 1. Sign up <br>2. Select compatibility quiz option <br>3. Select view quiz answers option | User is shown a message that they have not yet completed the compatibility quiz | User is shown a message that they need to complete the compatibility quiz | Pass |
| User takes compatibility quiz and finishes | 1. Select compatibility quiz option <br>2. Answer all questions | User is shown a message that they have completed the compatibility quiz | User is shown a message that they have completed the compatibility quiz | Pass |
| User views compatibility quiz answers after completing quiz | 1. Select compatibility quiz option <br>2. Select view quiz answers option | User is shown a message that they have not yet completed the compatibility quiz | User is shown a message that they have completed the compatibility quiz | Pass |
| User clicks "Return to main menu" on compatibility screen | 1. Select compatibility quiz option <br>2. Select return to main menu option | User is taken back to the main menu | User receives a message saying they are going back to main menu and is taken back to the main menu | Pass |
| User views matches without completing their profile but completed compatibility quiz | 1. Sign up <br>2. Select view matches option | User is shown a message that they need to fill out the genders seeking section | User is shown a message that they need to complete their profile | Pass |
| User clicks edit profile option | 1. Select edit profile option | User is taken to the edit profile screen | User is taken to the edit profile screen | Pass |
| User edits their profile and saves | 1. Select edit profile option <br>2. Edit profile details <br>3. Select save and exit option | User's profile is updated is taken back to the main menu | User is taken back to the main menu and profile is updated | Pass |
| User views messages without matching with anyone | 1. Sign up <br>2. Select view messages option | User is shown a message that they have no messages | User is shown a message that they have no messages | Pass |
| User views matches with matches | 1. Sign up <br>2. Complete profile and compatibility question <br>3. Select view matches option | User is shown a list of matches | User is shown a list of matches' names, age, gender, compatibility score and bio | Pass |
| User views messages with matches for first time | 1. View matches with complete profile (and have matches) <br>2. Select view messages option | User is prompted to allow for contact from that match | If match allows contact, displays message option. If match doesn't allow contact, displays message saying they have not yet allowed contact and redirects to matches screen. | Pass |
| User views messages with matches when contact is allowed | 1. View matches with complete profile (and have matches) <br>2. Select view matches option <br>3. Select a match that has allowed contact | User is shown a list of messages from that match and given the option to send a message | User is shown a list of messages from that match and given the option to send a message | Pass |
| User sends a message to the match | 1. View matches with complete profile (and have matches) <br>2. Select view matches option <br>3. Select a match that has allowed contact <br>4. Select send message option <br>5. Enter message | User's message is recorded and user is redirected to the match message screen where there is a list of messages from that match | User's message is saved with timestamp, message sent message is provided and the user is redirect back to the message with that match | Pass |
| User views all messages | 1. Select view matches option | User is shown a list of messages from all matches | User is shown a list of the most recent messages from all matches | Pass |
| User clicks logout option | 1. Select logout option | User is logged out and taken to the login/signup screen | User is logged out and taken to the login/signup screen | Pass |
| User logs in with incorrect usercode | 1. Select login option <br>2. Enter incorrect usercode | User is shown a message that the usercode is incorrect | User is shown a message that the usercode is incorrect | Pass |
| User logs in with incorrect password | 1. Select login option <br>2. Enter usercode <br>3. Enter incorrect password | User is shown a message that the password is incorrect | User is shown a message that the password is incorrect | Pass |
| User logs in with correct usercode and password | 1. Select login option <br>2. Enter usercode <br>3. Enter password | User is logged in and taken to the main menu | User is logged in and taken to the main menu | Pass |
| User forgets usercode | 1. Select the login option <br>2. Enter 'f' to indicate usercode was forgotten 3. Enter alias 4. Enter security questions correctly | User is presented with usercode | User is presented with usercode | Pass |
| User forgets password | 1. Select the login option <br>2. Enter the correct usercode <br>3. Enter 'f' to indicate password was forgotten <br>4. Enter security questions correctly <br>5. Enter new password | User's password is updated and they're brought back to the login screen | User's password is updated and they're brought back to the login screen | Pass |

## User testing

I shared the app with friends and family and asked them to test it. I asked them to test both the test user and real user versions of the app. I also shared the app in the Code Institute #peer-code-review channel and with my Code Institute cohort. I asked them to report any bugs they came acorss and to give feedback and the user experience. I used the feedback to make changes to the app. 

## User stories testing

#### As a first-time user, I want:

| User want | Action | Pass/Fail |
|------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| to be able to sign up for an account | After selecting whether they are a test user or a real user, the user is presented with a signup option. If they answer all the questions, they are signed up and logged in. | Pass |
| to be able to edit my profile | After logging in, the user is presented with a main menu. From there, they can choose to edit their profile. If they make changes to their profile, they are saved to the Google Sheet. | Pass |
| to be able to take a compatibility quiz | After logging in, the user is presented with a main menu. From there, they can choose to take the compatibility quiz. If they answer all the questions, their answers are saved to the Google Sheet. | Pass |
| to be able to view my matches | After logging in, the user is presented with a main menu. From there, they can choose to view their matches. If they have matches, they are presented with a list of their matches. | Pass |
| to be able to log out of my account | After logging in, the user is presented with a main menu. From there, they can choose to log out. If they choose to log out, they are logged out and taken back to the login/signup screen. | Pass |


#### As a returning user, I want:

| User want | Action | Pass/Fail |
|------------|--------|-----------|
| to be able to log in to my account | After selecting whether they are a test user or a real user, the user is presented with a login option. If they enter their usercode and password correctly, they are logged in and taken to the main menu. | Pass |
| to be able to edit my profile | After logging in, the user is presented with a main menu. From there, they can choose to edit their profile. If they make changes to their profile, they are saved to the Google Sheet. | Pass |
| to be able to view my messages | After logging in, the user is presented with a main menu. From there, they can choose to view their messages. If they have messages, they are presented with a list of their last message from each match. If they select a match, they are presented with a list of all the messages from that match. | Pass |
| to be able to message my matches | After logging in, the user is presented with a main menu. From there, they can choose to view their messages. If they have messages, they are presented with a list of their last message from each match. If they select a match, they are presented with a list of all the messages from that match. If they choose to send a message, they can type a message and send it to the match. The message is saved to the Google Sheet in the user and the match's message cell. | Pass |


#### As a frequent user, I want:

| User want | Action | Pass/Fail |
|------------|--------|-----------|
| to be able to edit my profile | The user can choose to edit their profile from the main menu. If they make changes to their profile, their answers are saved to the Google Sheet. | Pass |
| to be able to view my message history | The user can choose to view their messages. If they have messages, they are presented with a list of their last message from each match. If they select a match, they are presented with a list of all the messages from that match. Alternatively, they can view their matches and select the match to view their profile and then view their messages with the match. | Pass |
| to see new matches as they become available | The compatibility score is run each time the user views matches. If there are new users who are matches, or if someone has updated their preferences or compatibility test to match, they will be displayed in the matches list. | Pass |

## Code testing

I used the [Code Institute PEP8 validator](https://pep8ci.herokuapp.com/) to check my code for PEP8 compliance. I also used the [W3C Markup Validation Service](https://validator.w3.org/) to check my HTML for errors. I used the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/) to check my CSS for errors.


## Bugs and issues table

| Bug/Issue                                     | Potential Solution                    | Resolved Y/N | Additional Comments                                         |
|-----------------------------------------------------------------------------------|---------------------------------------------------------- |--------------|-----------------------------------------------------------------------------------------------------| 
| "Running startup command: python3 run.py" command appearing when app starts.   | Run command to clear console before app starts.      |   Y    | Resolved using the solution here: https://www.delftstack.com/howto/python/python-clear-console/   |
| For age input, any text input was breaking the app.                | Assert the type of the age variable.           |   Y    | I was able to resolve the issue by returning the function if necessary components were not met.   |
| When pulling a list from Google Sheets, the data passed back was a string.    | Convert the string to a list using the json module    |   Y    | I was able to resolve the issue by converting the string to a list using the json module.      |
| Data that has single quotes and doesn't work with json.loads           | Use a regex to replace single quotes           |   Y    | Used regex to replace single quotes at start and end of words and not within words         |
| The update genders method outputs each letter instead of each gender       | Use a regex to replace single quotes and use json.loads  |   Y    | Used regex to replace single quotes with double quotes for valid json string            |
| "IndexError: list index out of range" when sorting list by nested list value   | Change the reference to the list length          |   Y    | Changed `key=lambda x: x[2]` to `key=lambda x: x[1]`                        |
| Got a few circular import errors when trying to break down my classes       | Restructure so that classes don't import each other    |   Y    | When I had to call a function from another class, I instead passed a callback function to the class.|
| After completing or redoing the compatibility quiz, the answers aren't the user's | It could be that the value is being overwritten      |   Y    | When presenting the quiz options screen, I was using the existing instance's data instead      |
| 'User' is not subscriptable error when trying to access a user's matches     | Check the type of the user variable            |   Y    | I was able to resolve the issue updating the way I access the data within the user instance     |
| Mismatched ages depending on profile logged in as.                | Make sure the age is the right type            |   Y    | It turns out the user was checking if their own age was in range instead of the match's       |
| In the view all messages, the "last message from match" can be the user's message | Check for the True/False boolean when displaying message |   Y    | I looped through the messages to find the last one that the match sent instead           |
| When a newly signed up user logs out, they are unable to log back in       | Using the data before user existed in UserAccess class  |   Y    | Pulled the Google Worksheet data on the login/signup step                      |
| When updating user profile, a Gspread warning is displayed. Only applies to 6.0  | Catch the warning and ignore it              |   Y    | Imported warning module and ignored that warning to stop it from showing up             |
| If double quotes are added in a user message, it breaks.             | Remove double quotes before saving to the sheet.     |   Y    | Removed double quotes with .replace method                             |

## Known issues

- In the terminal, even though it is cleared, the user can still scroll up and see the previous output. The output is cut off so that it displays an earlier output than the last output on the screen. This appears to be an issue with the terminal.
- A feature that is partially a bug is that when the user changes their ages seeking, genders seeking or compatibility answers, matches who were once matches may no longer be displayed. However, the user can still contact them through the "View messages" setting if they have messages with that person already. I decided to leave that as is because it is like a real dating app where you can disconnect with someone but still have their message history. It also made me decide a good future-feature would be contact favouriting.

## Future features

- Add a way to favourite a match
- Add a way to block a match and prevent matching with them in the future
- Add a way to report a match (perhaps add reports to a new sheet)
- Add more compatibility quiz questions
- Notifications for new matches and new messages
- Colour indications of when contact is allowed
- Password encryption and hashing