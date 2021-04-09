
from init import UserSettings, UserSettingsSchema, get_config
from InquirerPy import inquirer
from utils.logs import err, warn
from wsock.wsock import *
from threading import Thread
from print_at import print_at
import uuid


class ClientInfo:
    def __init__(self, host: bool, username='', server_name=''):
        self.host = host

        self.username = username

        self.server_name = server_name

        self.address = ''


class Game:
    def __init__(self):

        self._user_requesting: list[UserSettings] = []

        self._opponent: UserSettings = None

        def _play_local_action():

            create_or_join_actions = {
                'Create a New Game': self._create_game,
                'Join a Game': self._join_game
            }

            create_or_join = inquirer.select('Create or Join a Game?', create_or_join_actions).execute()

            create_or_join_actions[create_or_join]()

        game_actions = {
            'Play Against a Friend Locally': _play_local_action,
            'Play Against a Friend Online': self._play_online,
            'Play Against a Bot': self._play_bot
        }

        action = inquirer.select('Choose how to play:', game_actions).execute()

        # Run the function
        game_actions[action]()

    def _create_game(self):

        # Start server with a timeout of 15 seconds
        server = Server(timeout=15)

        sock = WSock()

        token = uuid.uuid4().hex[:6]

        # sock.bind(token)
        # sock.subscribe(token)

        def _get_requests():
            while (True):
                opponent_info = sock.recv_json()

                self._user_requesting.append(opponent_info)

        t = Thread(target=_get_requests, daemon=True)

        t.start()

        print('Waiting for user to connect ...')
        while (True):
            user_requests = self._user_requesting
            # print(user_requests)

            if (len(user_requests) == 0):
                continue

            for user in user_requests:

                user = UserSettingsSchema().loads(user)

                accept = inquirer.text(
                    message=f'The user {user.username} is requesting to join, accept request?',
                    validate=lambda text: text.lower() in ['yes', 'no', 'n', 'y'],
                    invalid_message='Please answer with a yes or no'

                ).execute()

                print(accept)

                if (accept.lower() in ['yes', 'y']):
                    self._user_requesting = []
                    self._opponent = user

                    sock.send_str('Accepted', user.private_topic)
                    break

                else:
                    self._user_requesting.remove(user)

                    sock.send_str('Declined', user.private_topic)
                    break

    def _join_game(self):

        sock = WSock()

        settings = UserSettings(**get_config())

        priv_topic = settings.private_topic

        settings = UserSettingsSchema().dumps(settings)

        print(settings)

        sock.send_json(settings)

        x = sock.recv_str(priv_topic)

        print(x)

    def _play_online(self):
        warn('Implement Online')

    def _play_bot(self):
        warn('implement')
