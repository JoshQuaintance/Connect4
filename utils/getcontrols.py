from utils.getch import getch
from os import name
import keyboard

class _GetControls:
    def __init__(self, exit_only) -> None:
        self.exit_only = exit_only
        if name == 'nt':
            self.caller = _Windows()
        else:
            self.caller = _Unix()

    def __call__(self):
        return self.caller(self.exit_only)


class _Windows:
    def __call__(self, exit_only):
        retKey = ''

        first_ch = getch()

        # If CTRL + C is pressed
        if first_ch == b'\x03':
            exit()

        if exit_only:

            keyboard.press_and_release(first_ch.decode())

            return 'Not an exit key'

        else:

            if first_ch == b' ':
                retKey = 'SPACE_KEY'

            if first_ch == b'\r':
                retKey = 'ENTER_KEY'

            if first_ch == b'\x00' or first_ch == b'\xe0':

                key = getch()

                if key == b'H':
                    retKey = 'U_KEY'
                elif key == b'M':
                    retKey = 'R_KEY'
                elif key == b'P':
                    retKey = 'D_KEY'
                elif key == b'K':
                    retKey = 'L_KEY'

            return retKey


class _Unix:
    def __call__(self, exit_only):
        retKey = ''
        key = getch()

        # If CTRL + C is pressed
        if key == '\3':
            exit()

        if exit_only:

            keyboard.press_and_release(key.decode())

        else:

            if key == ' ':
                retKey = 'SPACE_KEY'

            if key == '\r':
                retKey = 'ENTER_KEY'

            if key == '\033':
                getch()

                arrow_key = getch()

                if arrow_key == 'A':
                    retKey = 'U_KEY'
                elif arrow_key == 'B':
                    retKey = 'D_KEY'
                elif arrow_key == 'C':
                    retKey = 'R_KEY'
                elif arrow_key == 'D':
                    retKey = 'L_KEY'

            return retKey


def getcontrols(exit_only):
    return _GetControls(exit_only)()
