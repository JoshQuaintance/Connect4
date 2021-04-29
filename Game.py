import threading

from board_old import Board
from init import UserSettings, UserSettingsSchema, get_config
from InquirerPy import inquirer
from utils.logs import err, warn
from wsock.wsock import *
from threading import Thread


class Game:
    def __init__(self):

        self._user_requesting: list[UserSettings] = []

        self._oponent = None

        self._user_conf = None

        self._port = None

        def _play_local_action():
            create_or_join_actions = {
                'Join a Game': self._join_game,
                'Create a New Game': self._create_game
            }

            while True:
                create_or_join = inquirer.select('Create or Join a Game?', create_or_join_actions).execute()

                response = create_or_join_actions[create_or_join]()

        game_actions = {
            'Play Against a Friend Locally': _play_local_action,
            # 'Play Against a Bot': self._play_bot
        }

        action = inquirer.select('Choose how to play:', game_actions).execute()

        # Run the function
        game_actions[action]()

    def _create_game(self):

        server = Server()

        user_conf = get_config()

        self._port = server.port

        print('In order for someone to join, they have to use this port below:')
        print(server.port)

        sock = WSock(user_conf, 'join', server.port)

        def _get_requests():
            while True:
                opponent_info_recv = sock.recv_json()

                if 'action' in opponent_info_recv and opponent_info_recv['action'] == 'exit':
                    exit(0)

                self._user_requesting.append(opponent_info_recv)

        get_req_t = Thread(target=_get_requests, daemon=True, name='Game._create_game._get_requests()')
        get_req_t.start()


        print('\rWaiting for a user to connect ...', end='')
        while True:

            if len(self._user_requesting) == 0:
                continue

            opponent_info = self._user_requesting[0]

            user = UserSettingsSchema().load(opponent_info)

            allow_user = inquirer.text(
                message=f'\nThe user "{user.username}" is requesting to join, accept request?',
                validate=lambda text: text.lower() in ['y', 'yes', 'no', 'n'],
                invalid_message='Please answer with a yes or no (y/n)'
            ).execute()

            if allow_user.lower() in ['yes', 'y']:

                self._oponent = user
                sock.send_str('accepted')
                break

            else:

                sock.send_str('declined')

                print(f'The user "{user.username}" is declined ...')
                print('\rWaiting for a user to connect ...', end='')

                del self._user_requesting[0]
                continue

        sock.send_json({'action': 'exit'})

        # ! Selecting which column of the number
        board = Board(self._port)
        board.draw_board()

        while True:
            key = getcontrols(False)

            if key == 'L_KEY' and board.highlighted > 1:
                board.highlighted -= 1
                board.draw_board()
                continue

            if key == 'R_KEY' and board.highlighted < 7:
                board.highlighted += 1
                board.draw_board()
                continue

            # If enter key is pressed, means something is selected
            if key == 'ENTER_KEY' or key == 'SPACE_KEY':
                # Change the selected into the highlighted
                board.selected = board.highlighted

                # Move
                board.move(board.selected)

                # Draw board
                board.draw_board()

                continue

    def _join_game(self):

        while True:
            try:
                user_conf = get_config()
                port = input('Enter in the port number to join: ')
                sock = WSock(user_conf, 'join', int(port))

                sock.send_json(UserSettingsSchema().dumps(user_conf))

                host_response = sock.recv_str()

                if host_response == 'declined':
                    print('The host declined you from joining the game ...')
                    return


            except Exception as e:
                if str(e) == 'Cannot Join, Game Started':
                    print(str(e))

                    return 'denied'

                elif str(e) == '[WinError 10061] No connection could be made because the target machine actively refused it':
                    print('Port doesn\'t have a server attached, please input a valid port ...')

                    return
                else:
                    print(e)

    def _play_bot(self):
        warn('implement')