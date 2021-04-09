
from InquirerPy import inquirer
from utils.logs import err, warn
from wsock.wsock import *


class ClientInfo:
    def __init__(self, host: bool, username='', server_name=''):
        self.host = host

        self.username = username

        self.server_name = server_name

        self.address = ''

        


class Game:
    def __init__(self):

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

        while (True):
            opponent_info = sock.recv_str()

    def _join_game(self):

        sock = WSock()

    def _play_online(self):
        warn('Implement Online')

    def _play_bot(self):
        warn('implement')
