
from init import UserSettings, UserSettingsSchema, get_config
from wsock.wsock_old import WSock, Server
from threading import Thread
from InquirerPy import inquirer


sock = WSock()

settings = UserSettings(**get_config())

priv_topic = settings.private_topic

settings = UserSettingsSchema().dumps(settings)

tkn = input('tkn: ')

sock.send_json(settings, tkn)
print('sent')

verification = sock.recv_str(priv_topic)

if (verification == 'declined'):
    print('Request to join was declined by host ...')