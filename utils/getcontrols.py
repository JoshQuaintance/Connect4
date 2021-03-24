from utils.getch import getch
from os import name


class _GetControls:
    def __init__(self) -> None:
        if name == 'nt':
            self.caller = _Windows()
        else:
            self.caller = _Unix()
    def __call__(self):
        return self.caller()

class _Windows:
    def __call__(self):
        retKey = ''
        
        first_ch = getch()

        if (first_ch == b'\r'):
            retKey = 'ENTER_KEY'

        if (first_ch == b'\x03'):
            exit()
        
        if (first_ch == b'\x00' or first_ch == b'\xe0'):

            key = getch()


            if (key == b'H'):
                retKey = 'U_KEY'
            elif (key == b'M'):
                retKey = 'R_KEY'
            elif (key == b'P'):
                retKey = 'D_KEY'
            elif (key == b'K'):
                retKey = 'L_KEY'
        
        return retKey

class _Unix:
    def __call__(self):
        retKey = ''
        key = getch()

        if (key == '\033'):
            getch()
    
            arrow_key = getch() 

            if (arrow_key == 'A'):
                retKey = 'U_KEY'
            elif (arrow_key == 'B'):
                retKey = 'R_KEY'
            elif (arrow_key == 'C'):
                retKey = 'D_KEY'
            elif (arrow_key == 'D'):
                retKey = 'L_KEY'
        
        return retKey

getcontrols = _GetControls()