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
        self.board_arr = [
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.']
        ]
        self.highest = [0, 0, 0, 0, 0, 0, 0]

        self.highlighted = 1

        self.turn = 1

        self.selected = 1
        self.last_move = None

        self.message = ''

        self.clear()

        # For testing purposes
        # self.board_arr = [
        #     ['.', '.', '.', '.', '.', '.', '.'],
        #     ['.', 'R', 'R', 'B', '.', '.', '.'],
        #     ['.', 'B', 'B', 'B', '.', '.', '.'],
        #     ['.', 'B', 'B', 'R', '.', '.', '.'],
        #     ['.', 'R', 'R', 'B', 'R', 'B', '.'],
        #     ['R', 'B', 'R', 'B', 'R', 'R', 'B']
        # ]

        # self.highest = [1, 5, 5, 5, 2, 2, 1]

    def clear(self):
        if sysname == 'nt':
            system('cls')
        else:
            system('clear')

    # Implement a move function that adds in blocks into the array
    def move(self, col):
        # Get the highest in the column
        highest_on_column = self.highest[col - 1]

        # Reset message
        self.message = ' ' * (len(self.message) + 2)

        # if the highest is bigger than 5, means board is full
        if (highest_on_column > 5):
            # Change the message that will be printed
            self.message = f'Column {col} is Full! Select a different column'
            # Break out
            return

        # Apply the 'R' or 'B' on selected column
        self.board_arr[5 - highest_on_column][col - 1] = 'R' if self.turn == 1 else 'B'

        # Change the highest into 1 more than before
        self.highest[col - 1] += 1

        # Change the turn
        self.turn = 1 if self.turn == 0 else 0

        # Change the lastMove
        self.last_move = self.selected

    def draw_board(self):
        # self.clear()

        # Add a newline at the top
        board_str = [['\n']]

        # ! MATH STUFF THAT I PROBABLY NEED TO EXPLAIN LATER
        board_str.append([' ' * (2) + ' ' * (4 * (self.highlighted - 1)) + colored('O', 'red' if self.turn == 1 else 'blue') + ' ' * 18])

        # print()
        board_str.append([f'{TOP_LEFT_CORNER}' + f'   {MIDDLE_CONNECT_DOWN}' * 6 + f'   {TOP_RIGHT_CORNER}'])

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
                    info_chosen = f'{"Blue" if self.turn == 1 else "Red"} Chose {self.last_move}' if self.last_move != None else f'{"":^35}'
                    board_row_str.append(f'{VERTICAL_LINE}{info_chosen:^35}{VERTICAL_LINE}\n')
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

        # Message
        board_str.append(self.message)

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

    # If enter key is pressed, means something is selected
    if (key == 'ENTER_KEY'):
        # Change the selected into the highlighted
        x.selected = x.highlighted

        # Move
        x.move(x.selected)

        # Draw board
        x.draw_board()
        continue
