
from init import UserSettings, UserSettingsSchema, get_config
from InquirerPy import inquirer, prompt
from utils.logs import err, warn
from wsock.wsock import *
from threading import Thread
import uuid


class ClientInfo:
    def __init__(self, host: bool, username='', server_name=''):
        self.host = host

        self.username = username

        self.server_name = server_name

        self.address = ''


class Game:
    def __init__(self):

        self._user_requesting: dict[int, UserSettings] = {
            
        }

        self._opponent: UserSettings = None

        def _play_local_action():

            create_or_join_actions = {
                'Create a New Game': self._create_game,
                'Join a Game': self._join_game
            }

            while (True):

                create_or_join = inquirer.select('Create or Join a Game?', create_or_join_actions).execute()

                response = create_or_join_actions[create_or_join]()

                if (create_or_join == 'Create a New Game'):
                    break
                else:
                    if (response == 'declined'):
                        continue
                    elif (response == 'accepted'):
                        break

                

        game_actions = {
            'Play Against a Friend Locally': _play_local_action,
            # 'Play Against a Friend Online': self._play_online,
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

        sock.bind(token)
        sock.subscribe(token)

        print('In order for someone to join, they have to use this token below:\n')
        print(token)

        def _get_requests():
            while (True):
                opponent_info = sock.recv_json()

                self._user_requesting[opponent_info.private_topic] = opponent_info

        t = Thread(target=_get_requests, daemon=True)

        t.start()

        print('Waiting for a user to connect ...')
        while (True):
            if (len(self._user_requesting) == 0):
                continue

            for user in self._user_requesting:

                user = UserSettingsSchema().loads(user)
                accept = ''

                while (True):
                    answer = input(f'The user "{user.username}" is requesting to join, accept request? ')

                    if (answer.lower() not in ['yes', 'y', 'n', 'no']):
                        print('Please answer with a yes or no (y or n)')
                        continue
                    else:
                        accept = answer
                        break

                if (accept.lower() in ['yes', 'y']):
                    self._user_requesting = []
                    self._opponent = user

                    sock.send_str('accepted', user.private_topic)
                    break

                else:

                    for i, user_info in enumerate(self._user_requesting):
                        user_info = UserSettingsSchema().loads(user_info)

                        print('USER_INFO\n', user_info.private_topic, '\n', user.private_topic)
                        if (user_info.private_topic == user.private_topic):
                            sock.send_str('declined', user.private_topic)
                            del self._user_requesting[i]
                            break


                    print(f'The user "{user.username}" is declined ...')
                    print('Waiting for a user to connect ...')

                    continue

    def _join_game(self):

        sock = WSock()

        settings = UserSettings(**get_config())

        priv_topic = settings.private_topic

        settings = UserSettingsSchema().dumps(settings)
        print('settings: ', settings)

        print('In order to join a match, you need to get an alphanumeric token. Ex: a56n1d')
        tkn = input('Input token here: ')

        sock.send_json(settings, tkn)

        verification = sock.recv_str(priv_topic)

        if (verification == 'declined'):
            print('Request to join was declined by host ...')
            return 'declined'

        else:
            return 'accepted'

    def _play_online(self):
        warn('Implement Online')

    def _play_bot(self):
        warn('implement')
