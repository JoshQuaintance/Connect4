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
    def __init__(self, room_tkn = ''):
        # 7 * 6 Board filled with dots meaning it's empty
        self.board_arr = [
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.']
        ]

        # The height of each column
        self.highest = [0, 0, 0, 0, 0, 0, 0]

        # The column currently being highlighted
        self.highlighted = 1

        # Player 1 will always be Red
        # name defaults to the color
        self.player_1 = 'Red'

        # Player 2 will always be blue
        # name defaults to the color
        self.player_2 = 'Blue'

        # Track how many moves there has been
        self.moves = 0

        # Who's turn it is
        # 1 = Red
        # 0 = Blue
        self.turn = 1

        # Room Token
        self.room_tkn = room_tkn or ''

        # Track how many rounds there has been
        # A round is if both players have moved
        self.round = 1

        # Selected column that will be used to fill up the board
        self.selected = 1

        # Track last move for info board
        self.last_move = None

        # If there is a message
        # This is because we are rewriting the buffer
        # So we have to clear it again if there is no message
        # Or it will stay
        self.message = ''

        # Makes sure it will clear the console on start
        self.clear()

        # A pre-created environment for testing purposes
        # self.board_arr = [
        #     ['.', '.', '.', '.', '.', '.', '.'],
        #     ['.', 'R', 'R', 'B', '.', '.', '.'],
        #     ['.', 'B', 'B', 'B', '.', '.', '.'],
        #     ['.', 'B', 'B', 'B', '.', '.', '.'],
        #     ['.', 'R', 'B', 'R', 'B', 'B', '.'],
        #     ['R', 'B', 'R', 'B', 'R', 'R', 'B']
        # ]
        # self.round = 3
        # self.highest = [1, 5, 5, 5, 2, 2, 1]
        # # # #

    def get_dynamic_shared(self):
        return {
            "board": self.board_arr,
            "moves": self.moves,
            "turn": self.turn,
            "round": self.round,
            "selected": self.selected,
            "last_move": self.last_move,
            "highlighted": self.highlighted
        }

    def init_shared_val(self):
        return {
            "player_1": self.player_1,
            "player_2": self.player_2
        }

    def clear(self):
        ''' Clears the console '''

        if sysname == 'nt':
            system('cls')
        else:
            system('clear')

    def move(self, col):
        ''' Implement a move function that adds in blocks into the array '''

        # Get the highest in the column
        highest_on_column = self.highest[col - 1]

        # Reset message, so the buffer will be reset too
        self.message = ' ' * (len(self.message) + 2)

        # if the highest is bigger than 5, means column is full
        if (highest_on_column > 5):
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
            self.check_win()

        # If the moves are even number
        if (self.moves % 2 == 0):

            # Increment the rounds, because
            # both players have moved
            self.round += 1

    def draw_board(self):
        ''' Function that draws the board '''

        # The board string array. Here we are using a method where
        # we construct the string first, then print it so it doesn't
        # flicker when we try to reprint the board. We add a newline
        # so the top of the baord won't be stuck to the top of the console
        board_str = [['\n']]

        # Adds the current color that is going to played on the top of the
        # column currently highlighted. It uses math that I really
        # do not feel like explaining it right now
        board_str.append([' ' * (2) + ' ' * (4 * (self.highlighted - 1)) +
                          colored('O', 'red' if self.turn == 1 else 'blue') + ' ' * 18])

        # Adds the top line to the array
        board_str.append([f'{TOP_LEFT_CORNER}' + f'   {MIDDLE_CONNECT_DOWN}' * 6 + f'   {TOP_RIGHT_CORNER}'])
        
        # A seperator between two rows where the characters lives
        # looks like this:
        ''' ┣   ╋   ╋   ╋   ╋   ╋   ╋   ┫ '''
        seperator = f'{MIDDLE_CONNECT_RIGHT}   ' + (f'{FOUR_WAY}   ') * 6 + MIDDLE_CONNECT_LEFT

        # Go through every row while enumerating it
        for i, row in enumerate(self.board_arr):

            # A string array for the current row
            board_row_str = []

            # Loop through the row
            for j in row:

                # Add the line where the character lives with it's colors if it applies
                board_row_str.append(f'{VERTICAL_LINE} {colored("O", "red") if j == "R" else colored("O", "blue") if j == "B" else j} ')

            # Close the line, then add 10 spaces for the infobox
            board_row_str.append(VERTICAL_LINE + ' ' * 10)

            # The width of the info box
            info_box_width = 35

            # Top line of the info box
            if (i == 0):
                board_row_str.append(f'{TOP_LEFT_CORNER}{HORIZONTAL_LINE * info_box_width}{TOP_RIGHT_CORNER}\n')
                board_row_str.append(seperator)
                board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

            # 2nd - 4th line
            elif (1 <= i < 5):
                if (i == 1):
                    room_info = f'Room Token: {self.room_tkn}' if self.room_tkn != '' else 'Local Room'
                    board_row_str.append(f'{VERTICAL_LINE}{room_info:^35}{VERTICAL_LINE}\n')
                    board_row_str.append(seperator)
                    board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

                elif (i == 2):
                    info_chosen = f'{colored("Blue", "blue") if self.turn == 1 else colored("Red", "red")} Chose {self.last_move}' if self.last_move != None else ''

                    if info_chosen == '':
                        board_row_str.append(f'{VERTICAL_LINE}{info_chosen:^35}{VERTICAL_LINE}\n')

                    else:
                        board_row_str.append(f'{VERTICAL_LINE}{info_chosen:^44}{VERTICAL_LINE}\n')
                    board_row_str.append(seperator)
                    board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

                elif (i == 3):
                    turn = f'{colored("Red", "red") if self.turn == 1 else colored("Blue", "blue")}'
                    info = 'It is ' + f'{turn:^5}' + '\'s turn'

                    board_row_str.append(VERTICAL_LINE + f"{info + '!':^44}" + VERTICAL_LINE + '\n')
                    board_row_str.append(seperator)
                    board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

                elif (i == 4):
                    board_row_str.append(VERTICAL_LINE + f'{f"Round {self.round}":^35}' + VERTICAL_LINE + '\n')
                    board_row_str.append(seperator)
                    board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

                else:
                    board_row_str.append(VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)
                    board_row_str.append(seperator)
                    board_row_str.append(' ' * 10 + VERTICAL_LINE + ' ' * info_box_width + VERTICAL_LINE)

            # Closer
            elif (i == 5):
                board_row_str.append(f'{BOTTOM_LEFT_CORNER}{HORIZONTAL_LINE * info_box_width}{BOTTOM_RIGHT_CORNER}\n')
                board_row_str.append(seperator)

            else:
                board_row_str.append(f'\n{MIDDLE_CONNECT_RIGHT}   ' + (f'{FOUR_WAY}   ') * 6 + MIDDLE_CONNECT_LEFT)

            board_str.append(board_row_str)

        # Last line
        board_str.append([f'{BOTTOM_LEFT_CORNER}' + (f'{HORIZONTAL_LINE * 3}' + MIDDLE_CONNECT_UP)
                          * 6 + f'{HORIZONTAL_LINE * 3}{BOTTOM_RIGHT_CORNER}'])

        # ? The selector is the highlighter
        # Top Selector
        _top = []
        for i in range(7):
            if (i + 1 == self.highlighted):
                _top.append(f'{D_TOP_LEFT_CORNER}   {D_TOP_RIGHT_CORNER}')
            else:
                _top.append('    ')

        board_str.append(_top)

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

    def get_full_row(self, row):
        # Gets the whole row
        return self.board_arr[row]

    def get_full_col(self, col):
        # Gets the whole column by going through every row and grab specific column
        # index and return it
        return [row[col] for row in self.board_arr]

    def get_full_diag_right(self, row, col):
        # If column is bigger than row (Top half of the board)
        if (col > row):

            # If the row and column points to an area with only 3 in diagonal length
            if (row <= 2 and col >= 4):

                # Return -1
                return ['']

            # Otherwise
            # Get the whole diagonal row to the right
            return [self.board_arr[j][i] for j, i in enumerate(range(col - row, 7))]

        # If the column is <= than row (Bottom half of the board)
        if (col <= row):

            # If the row and column points to an area with only 3 in diagonal length
            if (row >= 3 and col <= 2):

                # Return -1
                return ['']

            # Otherwise
            # Get the whole diagonal row to the right
            return [self.board_arr[row - col + i][i] for i in range(0, 6 - (row - col))]

    def get_full_diag_left(self, row, col):
        # If the diagonal length is less than 3
        if (row + col >= 9 or row + col <= 2):
            return ['']

        if (row + col >= 6):

            # ? THIS LOOKS INSANE AND I WOULD PROB FORGOT HOW IT WORKS
            # ? SO I'LL EXPLAIN THIS ONE
            # Lot's of 6s isn't there, the 6 is the width of the board
            # and if you're not me and wondering, Yes, it has to be in that order
            # Let's start on the range
            # 
            # ? Get where to stop
            # We get the distance from the column to 6 (This will get the most right corner)
            # Then subtract row with that number (This will get the starting row)
            # Then subtract 6 with that number (This will get the length of that diagonal)
            # Then subtract another 6 with that number (This will get the end of the diagonal)
            # 
            # ? What does the Enumerate do?
            # It basically acts as the start and incrementer for the row
            # Since the row will go up by one every time
            # basically, for every number created in the range
            # the enumerate function will make it into tuple
            # with the index of it. So like
            # 3, 4, 5 becomes (0, 3), (1, 4), (2, 5)
            # Then when getting the row subtract the sum of row and column
            # and subtract 6 from it to get the starting row.
            return [self.board_arr[j + (row + col - 6)][i] for j, i in enumerate(range(6, 6 - (6 - (row - (6 - col))), -1))]

        if (row + col < 6):
            return [self.board_arr[j][i] for j, i in enumerate(range(col + row, -1, -1))]

    def check_win(self, char=''):
        # If the character is not given, than check for who's turn it is
        if char == '':
            char = 'B' if self.turn == 1 else 'R'
        
        # Get the column
        col = self.selected - 1

        # Get the row
        row = 5 - self.highest[col] + 1

        # Create a local variable of the board
        board = self.board_arr

        get_around_highlighted = [self.get_full_row(row), self.get_full_col(col), self.get_full_diag_right(row, col), self.get_full_diag_left(row, col)]
        joined_stringified = [''.join(side) for side in get_around_highlighted]

        # Check if there is a 4 in a row
        if (any((char * 4) in side for side in joined_stringified)):

            # inform who won
            print(f'{colored("Blue", "blue") if self.turn == 1 else colored("Red", "red")} Won!')
            exit()

        # Check if there is any '.' inside the board (means it's empty)
        if (not any('.' in brd for brd in board)):

            # If there is it's a tie
            print('Tie')
            exit()


# ! Selecting which column of the number
x = Board('')
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
    if (key == 'ENTER_KEY' or key == 'SPACE_KEY'):
        # Change the selected into the highlighted
        x.selected = x.highlighted

        # Move
        x.move(x.selected)

        # Draw board
        x.draw_board()

        continue
