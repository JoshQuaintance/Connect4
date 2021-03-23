from utils.getarrow import getarrow
from os import system, name as sysname
from utils.drawingblocks import DrawingBlocks
from colorama import init
from termcolor import colored

init()

# ? THIS DECLARATIONS ARE BASICALL USELESS TO REMOVE WARNINGS
# ? It can also be used as a list of all the ASCII drawing
# ? Blocks used in this file
HORIZONTAL_LINE = None
VERTICAL_LINE = None
TOP_LEFT_CORNER = None
TOP_RIGHT_CORNER = None
BOTTOM_LEFT_CORNER = None
BOTTOM_RIGHT_CORNER = None
MIDDLE_CONNECT_LEFT = None
MIDDLE_CONNECT_RIGHT = None
FOUR_WAY = None
MIDDLE_CONNECT_UP = None
MIDDLE_CONNECT_DOWN = None
D_TOP_LEFT_CORNER = None
D_TOP_RIGHT_CORNER = None
D_BOTTOM_LEFT_CORNER = None
D_BOTTOM_RIGHT_CORNER = None

# Dynamically declares all the drawing blocks variables
for key, val in DrawingBlocks().getAll(return_format='dict').items():
    exec(f'{key}="{val}"')


class Board:
    def __init__(self):
        # 7 * 6 Board filled with Whatever is in the string
        # self.board_arr = [['.'] * 7] * 6

        # For testing purposes
        self.board_arr = [
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', 'R', 'R', 'B', '.', '.', '.'],
            ['.', 'B', 'R', 'B', '.', '.', '.'],
            ['.', 'B', 'B', 'R', '.', '.', '.'],
            ['.', 'R', 'R', 'B', 'R', 'B', '.'],
            ['.', 'B', 'R', 'B', 'R', 'R', 'B']
        ]

    def clear(self):
        if sysname == 'nt':
            system('cls')
        else:
            system('clear')

    def draw_board(self):
        self.clear()
        print()
        print(f'{TOP_LEFT_CORNER}' + f'   {MIDDLE_CONNECT_DOWN}' * 6 + f'   {TOP_RIGHT_CORNER}', end="top")

        print()

        for i, row in enumerate(self.board_arr):
            for j in row:
                print(f'{VERTICAL_LINE} {j} ', end="")
                # print('h')

            print(VERTICAL_LINE + str(i + i) + ' ' * 10, end="")

            if (i == 1):
                print(f'{TOP_LEFT_CORNER}{HORIZONTAL_LINE * 25}{TOP_RIGHT_CORNER}', end="\n")

            elif (2 <= i < 5):
                print(VERTICAL_LINE + ' ' * 10 + VERTICAL_LINE)

            else:
                print()

            print(f'{MIDDLE_CONNECT_RIGHT}   ' + (f'{FOUR_WAY}   ') * 6 + MIDDLE_CONNECT_LEFT + str(i + i + 1))

        # Last line
        print(f'{BOTTOM_LEFT_CORNER}' + (f'{HORIZONTAL_LINE * 3}' + MIDDLE_CONNECT_UP)
              * 6 + f'{HORIZONTAL_LINE * 3}{BOTTOM_RIGHT_CORNER}' + 'end')


x = Board()
x.draw_board()

while(True):
    key = getarrow()

    if (key == 'L_KEY' and x.selected > 1):
        x.selected -= 1
        x.draw_board()

    if (key == 'R_KEY' and x.selected < 7):
        x.selected += 1
        x.draw_board()
