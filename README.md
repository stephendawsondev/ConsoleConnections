# ConsoleConnections - CI PP3

## Resources used
- [TODOs in Python](https://www.jetbrains.com/help/pycharm/using-todo.html#view_todo)
- Lucidchart for flowcharts
- [Understanding Python Option arguments](https://realpython.com/python-optional-arguments/)
- [FreeCodeCamp Python Regex](https://www.freecodecamp.org/news/how-to-import-a-regular-expression-in-python/#howtousethepythonremodulewithregex)
- [Console Connections font](https://patorjk.com/software/taag/#p=display&h=2&v=1&f=NV%20Script&t=Console%20Connections)
- [Stackoverflow question on generating random numbers](https://stackoverflow.com/questions/2673385/how-to-generate-a-random-number-with-a-specific-amount-of-digits)
- [Code to clear the console](https://www.delftstack.com/howto/python/python-clear-console/)
- [Corey Schafer Python Tutorials on Classes](https://www.youtube.com/@coreyms)
- [update_cell method from gspread](https://docs.gspread.org/en/latest/user-guide.html)
- [json module in Python](https://docs.python.org/3/library/json.html)
- [re.sub() method explanation](https://www.pythontutorial.net/python-regex/python-regex-sub/)
- [Sorting list by nest list value - stackoverflow](https://stackoverflow.com/a/65679191/12297743)
- [Gspread user guide to update a full row](https://docs.gspread.org/en/latest/user-guide.html#updating-cells)
- [Avoiding circular imports](https://medium.com/brexeng/avoiding-circular-imports-in-python-7c35ec8145ed)
- [User is not subscriptable error explaination](https://blog.jcharistech.com/2022/02/07/how-to-fix-typeerror-object-is-not-subscriptable/)
## Planning

### Flowchart
<!-- Flowcharts to be added here -->

### Google sheet headings
Initial: usercode,	password, alias,	security_question_1,	security_answer_1, security_question_2,	security_answer_2,	bio,	gender,	genders_seeking,	age,	age_range_seeking,	messages_sent,	messages_received,	allow_contact_list,	question_1,	question_2,	question_3,	question_4,	question_5,	question_6,	question_7,	question_8,	question_9,	question_10	

Revision #1: usercode,	password,	alias,	security_questions,	age,	gender,	bio,	genders_seeking,	age_range_seeking,	messages_sent,	messages_received,	allow_contact_list,	compatibility_answers


## Bugs and issues

| Bug/Issue                                                                         | Potential Solution                                        | Resolved Y/N | Additional Comments                                                                                 |
|-----------------------------------------------------------------------------------|---------------------------------------------------------- |--------------|-----------------------------------------------------------------------------------------------------|  
| "Running startup command: python3 run.py" command appearing when app starts.      | Run command to clear console before app starts.           |      Y       | Resolved using the solution here: https://www.delftstack.com/howto/python/python-clear-console/     |
| For age input, any text input was breaking the app.                               | Assert the type of the age variable.                      |      Y       | I was able to resolve the issue by returning the function if necessary components were not met.     |
| When pulling a list from Google Sheets, the data passed back was a string.        | Convert the string to a list using the json module        |      Y       | I was able to resolve the issue by converting the string to a list using the json module.           |
| Data that has single quotes and doesn't work with json.loads                      | Use a regex to replace single quotes                      |      Y       | Used regex to replace single quotes at start and end of words and not within words                  |
| The update genders method outputs each letter instead of each gender              | Use a regex to replace single quotes and use json.loads   |      Y       | Used regex to replace signle quotes with double quotes for valid json string                        |
| "IndexError: list index out of range" when sorting list by nested list value      | Change the reference to the list length                   |      Y       | Changed `key=lambda x: x[2]` to `key=lambda x: x[1]`                                                |
| Got a few circular import errors when trying to break down my classes             | Restructure so that classes don't import each other       |      Y       | When I had to call a function from another class, I instead passed a callback function to the class.|
| After completing or redoing the compatibility quiz, the answers aren't the user's | It could be that the value is being overwritten           |      Y       | When presenting the quiz options screen, I was using the existing instance's data instead           |
| 'User' is not subscriptable error when trying to access a user's matches          | Check the type of the user variable                       |      Y       | I was able to resolve the issue updating the way I access the data within the user instance         |
| Mismatched ages depending on profile logged in as.                                | Make sure the age is the right type                       |      N       | It turns out the user was checking if their own age was in range instead of the match's             |    