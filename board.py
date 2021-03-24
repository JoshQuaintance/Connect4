from utils.getcontrols import getcontrols
from os import system, name as sysname
from utils.drawingblocks import DrawingBlocks
from colorama import init
from termcolor import colored
from time import sleep
from utils.getch import getch, _Getch
from print_at import print_at

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
        self.board_arr = [['.'] * 7] * 6

        self.highlighted = 1

        self.selected = 1
        self.clear()

        # For testing purposes
        # self.board_arr = [
        #     ['.', '.', '.', '.', '.', '.', '.'],
        #     ['.', 'R', 'R', 'B', '.', '.', '.'],
        #     ['.', 'B', 'B', 'B', '.', '.', '.'],
        #     ['.', 'B', 'B', 'R', '.', '.', '.'],
        #     ['.', 'R', 'R', 'B', 'R', 'B', '.'],
        #     ['.', 'B', 'R', 'B', 'R', 'R', 'B']
        # ]

    def clear(self):
        if sysname == 'nt':
            system('cls')
        else:
            system('clear')
    # ! Implement a move function that adds in blocks into the array
    # def move(self, col):

    def draw_board(self):
        # self.clear()

        board_str = [['\n']]

        # print()
        board_str.append([f'{TOP_LEFT_CORNER}' + f'   {MIDDLE_CONNECT_DOWN}' * 6 + f'   {TOP_RIGHT_CORNER}'])

        # print()

        seperator = f'{MIDDLE_CONNECT_RIGHT}   ' + (f'{FOUR_WAY}   ') * 6 + MIDDLE_CONNECT_LEFT

        for i, row in enumerate(self.board_arr):
            board_row_str = []
            for j in row:
                board_row_str.append(
                    f'{VERTICAL_LINE} {colored("O", "red") if j == "R" else colored("O", "blue") if j == "B" else j} ')

            board_row_str.append(VERTICAL_LINE + ' ' * 10)
            info_box_width = 35

            if (i == 1):
                board_row_str.append(f'{TOP_LEFT_CORNER}{HORIZONTAL_LINE * info_box_width}{TOP_RIGHT_CORNER}\n')
                board_row_str.append(seperator)
                board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

            elif (2 <= i < 4):
                if (i == 2):
                    board_row_str.append(VERTICAL_LINE + f'{"SOMEBODY CHOSE X or O":^35}' + VERTICAL_LINE + '\n')
                    board_row_str.append(seperator)
                    board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

                elif (i == 3):
                    board_row_str.append(VERTICAL_LINE + f'{"It is somebody turn":^35}' + VERTICAL_LINE + '\n')
                    board_row_str.append(seperator)
                    board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)
                else:
                    board_row_str.append(VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)
                    board_row_str.append(seperator)
                    board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

            elif (i == 4):
                board_row_str.append(f'{BOTTOM_LEFT_CORNER}{HORIZONTAL_LINE * info_box_width}{BOTTOM_RIGHT_CORNER}\n')
                board_row_str.append(seperator)

            else:
                board_row_str.append(f'\n{MIDDLE_CONNECT_RIGHT}   ' + (f'{FOUR_WAY}   ') * 6 + MIDDLE_CONNECT_LEFT)

            board_str.append(board_row_str)

        # Last line
        board_str.append([f'{BOTTOM_LEFT_CORNER}' + (f'{HORIZONTAL_LINE * 3}' + MIDDLE_CONNECT_UP)
                          * 6 + f'{HORIZONTAL_LINE * 3}{BOTTOM_RIGHT_CORNER}'])

        # selected = 2

        # Top Selector
        _top = []
        for i in range(7):
            if (i + 1 == self.highlighted):
                _top.append(f'{D_TOP_LEFT_CORNER}   {D_TOP_RIGHT_CORNER}')
            else:
                _top.append('    ')

        board_str.append(_top)
        # print()

        # Numbers
        _nums = []
        for i in range(7):
            _nums.append(f'  {i + 1} ')

        board_str.append(_nums)
        # print()

        # Bottom Selector
        _bottom = []
        for i in range(7):
            if (i + 1 == self.highlighted):
                _bottom.append(f'{D_BOTTOM_LEFT_CORNER}   {D_BOTTOM_RIGHT_CORNER}')
            else:
                _bottom.append('    ')
        board_str.append(_bottom)

        # Print the whole thing as a string
        print_at(1, 1, '\n'.join([''.join(row) for row in board_str]))


# ! Selecting which column of the number
x = Board()
x.draw_board()

while(True):
    key = getcontrols()

    if (key == 'L_KEY' and x.highlighted > 1):
        x.highlighted -= 1
        x.draw_board()
        continue

    if (key == 'R_KEY' and x.highlighted < 7):
        x.highlighted += 1
        x.draw_board()
        continue

    if (key == 'ENTER_KEY'):
        x.selected = x.highlighted
        break

print(f'{x.selected} is selected')
