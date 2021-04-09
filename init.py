import os
import json
import uuid
from marshmallow import Schema, fields, post_load

class UserSettingsSchema(Schema):
    username = fields.Str()
    default_server_namej = fields.Str()
    live_reload = fields.Bool()
    private_topic = fields.Str()

    # After the schema is
    @post_load
    def make_message(self, data, **__):
        print(data)
        return UserSettings(**data)

def default_conf():
    conf_content_warning = f'# DO NOT MODIFY THIS FILE UNLESS YOU KNOW WHAT YOU ARE DOING!'

    user_name = input('What do you want your username to be? ')

    default_server_name = input('What do you want your server name to default to? ')

    user_settings = {
        'username': user_name,
        'default_server_name': default_server_name,
        'live_reload': True
    }

    with open('config.toml', 'w') as fout:
        settings_data = json.dumps(user_settings)
        conf_settings_content = f'[user_settings]\n{settings_data}\n[end]'

        fout.write(conf_content_warning + '\n' + conf_settings_content)


def get_config():
        conf_file = open('config.toml')

        conf = conf_file.read()
        conf = conf.split('\n')

        conf_start = conf.index('[user_conf]')

        conf = conf[conf_start + 1]

        conf = json.loads(conf)

        # print(UserSettingsSchema().dumps((UserSettings(**conf))))

        return conf

class UserSettings:
    def __init__(self, username='', live_reload: bool = True, default_server_name='', private_topic=''):


        self.username = username

        self.default_server_name = default_server_name

        self.live_reload = live_reload

        self.private_topic = private_topic if private_topic != '' else uuid.uuid4().hex[:8]



def init():
    print('Initializing ...')

    print('Checking for config file. ...')

    if (not os.path.isfile('config.toml')):

        print('Config file not found!')
        print('Creating config file ...')

        default_conf()

    else:
        print('Config file exist, continueing ...')

        UserSettings()


# if __name__ == '__main__':
#     get_config()
