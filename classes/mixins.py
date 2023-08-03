import os


class ClearTerminalMixin():
    """
    Used in multiple files and clears the terminal when called.
    """
    @staticmethod
    def clear_terminal():
        """
        Clears the terminal window.
        """
        # https://www.delftstack.com/howto/python/python-clear-console/
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
