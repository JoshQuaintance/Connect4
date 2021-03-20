from os import system, name as sysname
from utils.drawingblocks import DrawingBlocks

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

# Dynamically declares all the drawing blocks variables
for key, val in DrawingBlocks().getAll(return_format='dict').items():
    exec(f'{key}="{val}"')


class Board:
    def __init__(self):
        # 7 * 6 Board filled with None
        self.board_arr = [[''] * 7] * 6

    def clear(self):
        if sysname == 'nt':
            system('cls')
        else:
            system('clear')

    def draw_board(self):

        print(VERTICAL_LINE, end="")
        print(chalk.red("R"))

        # print(f'{VERTICAL_LINE}   {VERTICAL_LINE}   {VERTICAL_LINE}')
        # print(f'{MIDDLE_CONNECT_RIGHT}   {FOUR_WAY}   {MIDDLE_CONNECT_LEFT}')
        # print(f'{VERTICAL_LINE} {chalk.red("R")} {VERTICAL_LINE}   {VERTICAL_LINE}')
        # print(f'{BOTTOM_LEFT_CORNER}{HORIZONTAL_LINE * 3}{MIDDLE_CONNECT_UP}{HORIZONTAL_LINE * 3}{BOTTOM_RIGHT_CORNER}')


x = Board()
x.draw_board()
