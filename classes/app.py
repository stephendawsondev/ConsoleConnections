from classes.mixins import ClearTerminalMixin
from classes.user_access import UserAccess

CONSOLE_CONNECTIONS_HEADING = """
                ,gggg,
               ,88^^^Y8b,                                           ,dPYb,
              d8"     `Y8                                           IP'`Yb
             d8'   8b  d8                                           I8  8I
            ,8I    "Y88P'                                           I8  8'
            I8'           ,ggggg,   ,ggg,,ggg,    ,g,      ,ggggg,  I8 dP  ,ggg,
            d8           dP"  "Y8gg,8" "8P" "8,  ,8'8,    dP"  "Y8ggI8dP  i8" "8i∂
            Y8,         i8'    ,8I I8   8I   8I ,8'  Yb  i8'    ,8I I8P   I8, ,8I
            `Yba,,_____,d8,   ,d8',dP   8I   Yb,8'_   8),d8,   ,d8',d8b,_ `YbadP'
              `"Y,gggg,P"Y8888P"  8P'   8I   `YP' "YY8P8P"Y8888P"  8P'"Y8888P"Y888
     ,gggg,
   ,88^^^Y8b,                                                      I8
  d8"     `Y8                                                      I8
 d8'   8b  d8                                                   88888888gg
,8I    "Y88P'                                                      I8   ""
I8'           ,ggggg,   ,ggg,,ggg,   ,ggg,,ggg,   ,ggg,    ,gggg,  I8   gg    ,ggggg,   ,ggg,,ggg,    ,g,
d8           dP"  "Y8gg,8" "8P" "8, ,8" "8P" "8, i8" "8i  dP"  "Yb I8   88   dP"  "Y8gg,8" "8P" "8,  ,8'8,
Y8,         i8'    ,8I I8   8I   8I I8   8I   8I I8, ,8I i8'      ,I8,  88  i8'    ,8I I8   8I   8I ,8'  Yb
`Yba,,_____,d8,   ,d8',dP   8I   Yb,dP   8I   Yb,`YbadP',d8,_    ,d88b_,88,,d8,   ,d8',dP   8I   Yb,8'_   8)
  `"Y888888P"Y8888P"  8P'   8I   `Y8P'   8I   `Y888P"Y88P""Y8888P8P""Y8P""YP"Y8888P"  8P'   8I   `YP' "YY8P8P """


APP_SUBHEADING = "\t\t\t\t\u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764\n\n\t\t\t\tThere's no cover to judge here!\n\n\t\t\t\t\u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764 \u2764\n"


class App():
    """
    The top level class for the app.
    - Starts the app
    """

    def __init__(self):
        self.start_app()

    ClearTerminalMixin.clear_terminal()

    def present_app_heading(self):
        """
        Displays the app heading.
        """
        print(
            f"t\t\t\t\t\tWelcome to\n\n{CONSOLE_CONNECTIONS_HEADING}\n{APP_SUBHEADING}")

    def start_app(self):
        """
        Starts the app.
        - Displays the app heading.
        - Establishes the user data.
        """
        user_access = UserAccess()
        self.present_app_heading()
        return user_access.establish_user_data()
