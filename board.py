from types import SimpleNamespace

from utils.getcontrols import getcontrols
from os import system, name as sysname
from utils.drawingblocks import *
from colorama import init
from termcolor import colored
from time import sleep
from utils.getch import getch, _Getch
from print_at import print_at

init()


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

        self._board_str = [
            ' ' * 80,  # Row 1
            ' ' * 80,  # Row 2
            ' ' * 80,  # Row 3
            ' ' * 80,  # Row 4
            ' ' * 80,  # Row 5
            ' ' * 80,  # Row 6
            ' ' * 80,  # Row 7
            ' ' * 80,  # Row 8
            ' ' * 80,  # Row 9
            ' ' * 80,  # Row 10
            ' ' * 80,  # Row 11
            ' ' * 80,  # Row 12
            ' ' * 80,  # Row 13
            ' ' * 80,  # Row 14
            ' ' * 80,  # Row 15
            ' ' * 80,  # Row 16
            ' ' * 80,  # Row 17
            ' ' * 80,  # Row 18
            ' ' * 80,  # Row 19
            ' ' * 80,  # Row 20
            ' ' * 80,  # Row 21
            ' ' * 80,  # Row 22
            ' ' * 80,  # Row 23
            ' ' * 80,  # Row 24
            ' ' * 80  # Row 25
        ]

        # The height of each column
        self.highest = [0, 0, 0, 0, 0, 0, 0]

        # The column currently being highlighted
        self.highlighted = 1

        self.player_1 = 'Red'

        self.player_2 = 'Blue'

        self.moves = 0

        self.turn = 1

        self.room_port = room_port

        self.round = 1

        self.selected = 1

        self.last_move = None

        self.info_box = SimpleNamespace(**{
            'width': 38,
            'height': 12,
            'room_port': self.room_port,
            'round': self.round,
            'turn': self.turn
        })

        self.clear_screen()

        # A pre-created environment for testing purposes
        # self.board_arr = [
        #     ['.', '.', 'B', 'R', '.', '.', '.'],
        #     ['.', 'R', 'R', 'B', '.', '.', '.'],
        #     ['.', 'B', 'B', 'B', '.', '.', '.'],
        #     ['.', 'B', 'B', 'B', '.', '.', '.'],
        #     ['.', 'R', 'B', 'R', 'B', 'B', '.'],
        #     ['R', 'B', 'R', 'B', 'R', 'R', 'B']
        # ]
        # self.round = 3
        # self.highest = [1, 5, 5, 5, 2, 2, 1]

    def clear_screen(self):
        """ Clears the console """

        if sysname == 'nt':
            system('cls')
        else:
            system('clear')

    def clear_line(self, line):
        if 0 > line > 30:
            raise ValueError('Line number must be 0 <= line <= 30')

        self._board_str[line] = ' ' * 80

        return

    def clear_board(self):
        self._board_str = [
            ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80,
            ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80,
            ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80, ' ' * 80
        ]

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

        if 0 > col > 80 or 0 > row > 30:
            raise ValueError('Coordinates must be (0 <= row <= 30, 0 <= col <= 80)')

        # print(string, len(string), len(color) if color is not None else '')

        if len(string) > 80:
            raise ValueError('String must be ≤ 80 characters')

        # These two variables make sure that the string won't go over 80 characters
        end = col + len(string) + 1 if col + len(string) + 1 <= 80 else 80
        beg = col if col + len(string) + 1 <= 80 else col - len(string)

        self._board_str[row] = self._board_str[row][:beg] + string + self._board_str[row][end:]

        return

    def move(self, col):

        # Get the highest in the column
        highest_on_column = self.highest[col - 1]

        self.clear_line(16)

        # if the highest is bigger than 5, means column is full
        if highest_on_column > 5:
            # Change the message that will be printed
            self.put_str(f'Column {col} is Full! Select a different column', (16, 0))

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

    def create_board(self):

        self.highlighted = 4

        self.put_str(colored('O', 'red' if self.turn == 1 else 'blue'), (0, 2 + 4 * (self.highlighted - 1)))

        for i in range(1, 8):
            self.put_str(str(i), (16, 2 + 4 * (i - 1)))

        # Top Row of the board
        self.put_str(TOP_LEFT_CORNER, (1, 0))

        for i in range(1, 7):
            self.put_str(MIDDLE_CONNECT_DOWN, (1, i * 4))

        self.put_str(TOP_RIGHT_CORNER, (1, 28))

        # Middle Areas
        for row, i in enumerate(range(2, 13, 2)):

            input_str = f""
            for col in self.board_arr[row]:
                input_str += f'{VERTICAL_LINE} {col} '

            self.put_str(f"{input_str}{VERTICAL_LINE}", (i, 0))

        for i in range(2, 13, 2):

            for j in range(1, 7):
                self.put_str(FOUR_WAY, (i + 1, 1 + (j * 4)))

            self.put_str(MIDDLE_CONNECT_RIGHT, (i + 1, 0))
            self.put_str(MIDDLE_CONNECT_LEFT, (i + 1, 28))

        self.put_str(BOTTOM_LEFT_CORNER, (14, 0))
        self.put_str(HORIZONTAL_LINE * 27, (14, 1))
        self.put_str(BOTTOM_RIGHT_CORNER, (14, 28))

        self.put_str(f'Column {5} is Full! Select a different column', (18, 0))

    def create_info_box(self):

        props = self.info_box

        for i in range(props.height - 1):
            self.put_str(f"{VERTICAL_LINE}{' ' * 38}{VERTICAL_LINE}", (i + 2, 38))

        self.put_str(f"{TOP_LEFT_CORNER}{HORIZONTAL_LINE * props.width}{TOP_RIGHT_CORNER}", (1, 38))
        self.put_str(
            f"{BOTTOM_LEFT_CORNER}{HORIZONTAL_LINE * props.width}{BOTTOM_RIGHT_CORNER}",
            (1 + props.height, 38)
        )

        self.put_str(
            f"{('Local Room' if props.room_port is None else 'Room Token: '+str(props.room_port)):^38}{VERTICAL_LINE}",
            (2, 39)
        )

    def edit_info_box(self):
        pass

    def highlight_column(self, col):
        self.highlighted = col

        self.put_str(f'{DrawingBlocks().double_namespace.D_TOP_LEFT_CORNER}   {D_TOP_RIGHT_CORNER}', (15, col * 4))

    def draw_board(self):

        self.create_board()
        self.create_info_box()
        self.highlight_column(1)

        # Parses the color
        for i, row in enumerate(self._board_str):
            self._board_str[i] = \
                row[:30].replace('B', colored('O', 'blue')).replace('R', colored('O', 'red'), 7) + \
                row[30:]

        concat_board_str = ''

        for rows in self._board_str:
            concat_board_str += rows + '\n'

        print('1234567890' * 8)
        print(concat_board_str)


board = Board(8665)

board.draw_board()
