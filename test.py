
from init import UserSettingsSchema
from wsock.wsock import WSock, Server
from threading import Thread
from InquirerPy import inquirer
import uuid

server = Server(timeout=15)

sock = WSock()
oponent = None
clis = []

token = uuid.uuid4().hex[:6]

sock.bind(token)
sock.subscribe(token)

print('In order for someone to join, they have to use this token below:\n')
print(token)

def _req_handler():
    while (True):
        op_info = vars(sock.recv_json())

        clis.append(op_info)


Thread(target=_req_handler, daemon=True).start()

while (True):
    if (len(clis) == 0):
        continue

    op_info = clis[0]
    print(op_info)

    user = UserSettingsSchema().load(op_info)

    allow_user = inquirer.text(
        message=f'\nThe user "{user.username}" is requesting to join, accept request?',
        validate= lambda text: text.lower() in ['y', 'yes', 'n', 'no'],
        invalid_message= 'Please answer with a yes or no (y/n)'
    ).execute()

    if (allow_user.lower() in ['yes', 'y']):

        oponent = user
        sock.send_str('accepted', user.private_topic)
        break
    else:
        sock.send_str('declined', user.private_topic)

        print(f'The user "{user.username}" is declined ...')
        print('\rWaiting for a user to connect ...', end='')

        del clis[0]
        continue
