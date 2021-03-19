"""
NOTE    
On this file, there is going to be warnings of undeclared variables. If it's 
because of the ASCII drawing lines, ignore it, because it's getting declared on runtime
"""

import PyInquirer as inquirer
from drawingblocks import DrawingBlocks
from os import name, system
from prompt import choose
from logs import err, warn

# ? THIS DECLARATIONS ARE BASICALL USELESS TO REMOVE WARNINGS
# ? It can also be used as a list of all the ASCII drawing
# ? Blocks used in this file
HORIZONTAL_LINE = None
VERTICAL_LINE = None
TOP_LEFT_CORNER = None
TOP_RIGHT_CORNER = None
BOTTOM_LEFT_CORNER = None
BOTTOM_RIGHT_CORNER = None


# Dynamically declares all the drawing blocks variables
for key, val in DrawingBlocks().getAll(return_format='dict').items():
    exec(f'{key}="{val}"')


class Menu:
    def clear(self):
        if name == 'nt':
            system('cls')
        else:
            system('clear')

    def print_title(self):
        '''
        Prints out menu title

        Prints Out
        ------
        ```
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃                                  ┃
        ┃                                  ┃
        ┃           Connect Four           ┃
        ┃          Joshua Pelealu          ┃
        ┃                                  ┃
        ┃                                  ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
        ```
        '''

        # Clears the console
        self.clear()

        print(f"{ TOP_LEFT_CORNER }{ HORIZONTAL_LINE * 34 }{ TOP_RIGHT_CORNER }")
        print(f"{VERTICAL_LINE}                                  {VERTICAL_LINE}")
        print(f"{VERTICAL_LINE}                                  {VERTICAL_LINE}")
        print(f"{VERTICAL_LINE}           Connect Four           {VERTICAL_LINE}")
        print(f"{VERTICAL_LINE}                by                {VERTICAL_LINE}")
        print(f"{VERTICAL_LINE}          Joshua Pelealu          {VERTICAL_LINE}")
        print(f"{VERTICAL_LINE}                                  {VERTICAL_LINE}")
        print(f"{VERTICAL_LINE}                                  {VERTICAL_LINE}")
        print(f"{ BOTTOM_LEFT_CORNER }{ HORIZONTAL_LINE * 34 }{ BOTTOM_RIGHT_CORNER }")

    def print_main_menu(self):
        print()
        print(f'{"Main Menu":^}')
        print()

        availableActions = ['Start a New Game', 'Setting Options', 'Quit']

        user_action = choose('Choose an action:', availableActions)

        if (user_action == availableActions[2]):
            print('Exiting ...')
            exit()

        if (user_action == availableActions[0]):
            warn('IMPLEMENT A PLAY GAME')

        if (user_action == availableActions[1]):
            warn('Settings')