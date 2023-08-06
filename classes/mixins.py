import os
import time


class ClearTerminalMixin():
    """
    Used in multiple files and clears the terminal when called.
    """
    @staticmethod
    def clear_terminal(delay=0):
        """
        Clears the terminal window.
        """
        time.sleep(delay)
        # https://www.delftstack.com/howto/python/python-clear-console/
        command = 'clear'
        if os.name in (
                'nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
