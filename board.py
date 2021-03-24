from getarrow import getarrow
from utils.getarrow import getarrow
from os import system, name as sysname
from utils.drawingblocks import DrawingBlocks
from colorama import init
from termcolor import colored
from time import sleep
from utils.getch import getch, _Getch


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
<< << << < HEAD
D_TOP_LEFT_CORNER = None
D_TOP_RIGHT_CORNER = None
D_BOTTOM_LEFT_CORNER = None
D_BOTTOM_RIGHT_CORNER = None
== == == =
D_TOP_LEFT_CORNER = None
D_TOP_RIGHT_CORNER = None
D_BOTTOM_LEFT_CORNER = None
D_BOTTOM_RIGHT_CORNER = None
>>>>>> > pynput

# Dynamically declares all the drawing blocks variables
for key, val in DrawingBlocks().getAll(return_format='dict').items():
    exec(f'{key}="{val}"')


class Board:
    def __init__(self):
        # 7 * 6 Board filled with Whatever is in the string
        # self.board_arr = [['.'] * 7] * 6

        self.selected = 1

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
        print(f'{TOP_LEFT_CORNER}' + f'   {MIDDLE_CONNECT_DOWN}' * 6 + f'   {TOP_RIGHT_CORNER}', end="")

        print()

        seperator = f'{MIDDLE_CONNECT_RIGHT}   ' + (f'{FOUR_WAY}   ') * 6 + MIDDLE_CONNECT_LEFT

        for i, row in enumerate(self.board_arr):
            for j in row:
                print(f'{VERTICAL_LINE} {j} ', end="")
                # print('h')

            print(VERTICAL_LINE + ' ' * 10, end="")
            info_box_width = 35

            if (i == 1):
                print(f'{TOP_LEFT_CORNER}{HORIZONTAL_LINE * info_box_width}{TOP_RIGHT_CORNER}', end="\n")
                print(seperator, end="")
                print(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

            elif (2 <= i < 4):
                if (i == 2):
                    print(VERTICAL_LINE + f'{"SOMEBODY CHOSE X or O":^35}' + VERTICAL_LINE)
                    print(seperator, end="")
                    print(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

                elif (i == 3):
                    print(VERTICAL_LINE + f'{"It is somebody turn":^35}' + VERTICAL_LINE)
                    print(seperator, end="")
                    print(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)
                else:
                    print(VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)
                    print(seperator, end="")
                    print(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

            elif (i == 4):
                print(f'{BOTTOM_LEFT_CORNER}{HORIZONTAL_LINE * info_box_width}{BOTTOM_RIGHT_CORNER}', end="\n")
                print(seperator)

            else:

                print()
                print(f'{MIDDLE_CONNECT_RIGHT}   ' + (f'{FOUR_WAY}   ') * 6 + MIDDLE_CONNECT_LEFT)

        # Last line
        print(f'{BOTTOM_LEFT_CORNER}' + (f'{HORIZONTAL_LINE * 3}' + MIDDLE_CONNECT_UP)
              * 6 + f'{HORIZONTAL_LINE * 3}{BOTTOM_RIGHT_CORNER}')

        # selected = 2

        # Top Selector
        for i in range(7):
            if (i + 1 == self.selected):
                print(f'{D_TOP_LEFT_CORNER}   {D_TOP_RIGHT_CORNER}', end="")
            else:
                print('    ', end="")

        print()

        # Numbers
        for i in range(7):
            print(f'  {i + 1} ', end='')

        print()

        # Bottom Selector
        for i in range(7):
            if (i + 1 == self.selected):
                print(f'{D_BOTTOM_LEFT_CORNER}   {D_BOTTOM_RIGHT_CORNER}', end="")
            else:
                print('    ', end="")


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
