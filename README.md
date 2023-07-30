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

## Planning

### Flowchart
<!-- Flowcharts to be added here -->

### Google sheet headings
Initial: usercode,	password, alias,	security_question_1,	security_answer_1, security_question_2,	security_answer_2,	bio,	gender,	genders_seeking,	age,	age_range_seeking,	messages_sent,	messages_received,	allow_contact_list,	question_1,	question_2,	question_3,	question_4,	question_5,	question_6,	question_7,	question_8,	question_9,	question_10	

Revision #1: usercode,	password,	alias,	security_questions,	age,	gender,	bio,	genders_seeking,	age_range_seeking,	messages_sent,	messages_received,	allow_contact_list,	compatibility_answers


## Bugs and issues

| Bug/Issue                                                                   | Potential Solution                             | Resolved Y/N  | Additional Comments                                                                                 |
|-----------------------------------------------------------------------------|------------------------------------------------|---------------|-----------------------------------------------------------------------------------------------------|
| "Running startup command: python3 run.py" command appearing when app starts | Run command to clear console before app starts | Y             | Resolved using the solution here: https://www.delftstack.com/howto/python/python-clear-console/     |
| For age input, any text input was breaking the app                          | Assert the type of the age variable            | Y             | I was able to resolve the issue by returning the function if necessary components were not met.     |