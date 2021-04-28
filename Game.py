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

        print('In order for someone to join, they have to use this port below:')
        print(server.port)

        sock = WSock(user_conf, 'join', server.port)

        def _get_requests():
            while True:
                opponent_info_recv = sock.recv_json()

                self._user_requesting.append(opponent_info_recv)

        Thread(target=_get_requests, daemon=True, name='Game._create_game._get_requests()').start()

        print('\rWaiting for a user to connect ...', end='')
        while True:

            if len(self._user_requesting) == 0:
                continue

            opponent_info = self._user_requesting[0]

            user = UserSettingsSchema().load(opponent_info)

            allow_user = inquirer.text(
                message=f'\nThe user"{user.username}" is requesting to join, accept request?',
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

    def _join_game(self):

        while True:
            try:
                user_conf = get_config()
                port = input('Enter in the port number to join: ')
                sock = WSock(user_conf, 'join', int(port))

                print('yessssssss')

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