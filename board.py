from types import SimpleNamespace

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
    def __init__(self, room_port=None):
        self.board_arr = [
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.']
        ]

        self._board_str = {
            0: ' ' * 80,
            1: ' ' * 80,
        }

        # The height of each column
        self.highest = [0, 0, 0, 0, 0, 0, 0]

        # The column currently being highlighted
        self.highlighted = 1

        self.player_1 = 'Red'

        self.player_2 = 'Blue'

        self.moves = 0

        self.turn = 0

        self.room_port = room_port

        self.round = 1

        self.selected = 1

        self.last_move = None

        # Message row is at row 20
        self.message = ''

        self.clear()

    def clear(self):
        """ Clears the console """

        if sysname == 'nt':
            system('cls')
        else:
            system('clear')

    def move(self, col):

        # Get the highest in the column
        highest_on_column = self.highest[col - 1]

        # if the highest is bigger than 5, means column is full
        if highest_on_column > 5:
            # Change the message that will be printed
            self.message = f'Column {col} is Full! Select a different column'

            # Break out of the function
            return

        # Apply the 'R' or 'B' on selected column
        self.board_arr[5 - highest_on_column][col - 1] = 'R' if self.turn == 1 else 'B'

        # CIncrement the highest in the column
        self.highest[col - 1] += 1

        # Change who's turn it is
        self.turn = 1 if self.turn == 0 else 0

        # Increment the amount of moves
        self.moves += 1

        # Apply the selected column into the last move
        self.last_move = self.selected

        # If it has been more than 3 rounds
        if self.round > 3:
            # Draw the board first so if there is a win
            # it will draw it first before exitting
            self.draw_board()

            # Then we can check for win
            # self.check_win()

        # If the moves are even number
        if self.moves % 2 == 0:
            # Increment the rounds, because
            # both players have moved
            self.round += 1

    def put_str(self, string: str, coord: tuple[int, int]) -> None:
        """
        Puts string into the board at specific coordinate\n
        If there is an existing string, it will override it

        Parameters
        ----------
        string : String to put into the board
        coord  : Coordinate where the string is to be put
        """
        row, col = coord

        if 0 > col > 80 or 0 > row > 20:
            raise ValueError('Coordinates must be (0 <= row <= 20, 0 <= col <= 80)')

        if len(string) > 80:
            raise ValueError('String must be ≤ 80 characters')

        # These two variables make sure that the string won't go over 80 characters
        end = col + len(string) + 1 if col + len(string) + 1 <= 80 else 80
        beg = col if col + len(string) + 1 <= 80 else col - len(string)

        self._board_str[row] = self._board_str[row][:beg] + string + self._board_str[row][end:]

        return

    def draw_board(self):

        board_str = self._board_str

        self.put_str('Hello', (1, 0))
        self.put_str('World', (1, 6))

        concat_board_str = ''

        for _key, _val in board_str.items():
            concat_board_str += _val + '\n'

        print('1234567890' * 8)
        print(concat_board_str)


board = Board(8665)

board.draw_board()
