import socket
import json
from marshmallow import Schema, fields, post_load
import os
from threading import Thread
import functools


class MessageSchema(Schema):
    content = fields.Str()

    content_type = fields.Str()

    @post_load
    def make_message(self, data, **__):
        return Message(**data)()


class Message:
    def __init__(self, content, content_type):
        self.content = content

        self.content_type = content_type

    # If the class is called as a function
    def __call__(self):

        # The parse the content
        self.content = self.parse_content()

        # And return the whole class
        return self

    # Parses the content
    def parse_content(self):
        if self.content_type == 'str':
            self.content = str(self.content)
            return self.content

        else:

            if type(self.content) == str:
                self.content = json.loads(self.content)

                return self.content

            return self.content


class Server:
    def __init__(self):

        self._clients = []
        self._clients_info = {}
        self._message_queue = []
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = '127.0.0.1'
        self._port = 8665

        self._config = {
            'status': 'looking',  # 'looking' | 'playing'
        }

        # Avoids port conflict
        while True:
            try:
                # Try binding the socket to the default current configured port
                self._sock.bind((self._host, self._port))

            except OSError as e:
                # If it raised an 'Address already in use'
                if str(e) == '[Errno 98] Address already in use':

                    # increment the port and continue the run
                    self._port += 1

                    continue

                else:
                    # Otherwise, re throw the exception
                    raise e

            else:
                break

        self._sock.listen()

        Thread(target=self._start_server, daemon=True).start()
        Thread(target=self._message_sender, daemon=True).start()

    def _start_server(self):
        """ Starts the server """

        from threading import Thread

        sock = self._sock

        while True:
            c, addr = sock.accept()

            self._clients.append((c, addr))

            Thread(target=self._client_handler, args=(c, addr), daemon=True).start()

    def _client_handler(self, c, addr):
        """ Handles clients receiving and sending data """

        try:
            while True:
                # Get data from client
                data = c.recv(1024)

                if not data:
                    continue

                data = data.decode()

                if 'sock_conn_init' in data:
                    parsed = json.loads(data)

                    if parsed['intent'] == 'join' and self._config['status'] != 'looking':
                        c.send(bytes('no joining', 'utf-8'))

                        self._clear_client(addr)
                        exit(0)

                    parsed_info = json.loads(parsed['client_info'])

                    self._clients_info[addr] = parsed_info

                    continue

                else:
                    data = data.encode()

                self._message_queue.append((addr, data))

        except Exception as e:
            raise e

    def _message_sender(self):

        while True:
            if len(self._message_queue) == 0:
                continue

            sender_addr, message = self._message_queue[0]

            for client, address in self._clients:

                if address != sender_addr:
                    try:
                        client.sendall(message)

                    except Exception as e:
                        raise e

            del self._message_queue[0]

    def _clear_client(self, addr):

        for client, address in self._clients:

            if address == addr:
                self._clients.remove((client, address))

                break

        self._clients_info.pop(addr, None)


class WSock:

    def __init__(self, user_conf, intent, port=None):

        self._port = port if port is not None else 8765

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect(('127.0.0.1', self._port))
        self._user_conf = user_conf

        init_message = {
            'sock_conn_init': True,
            'user_conf'     : user_conf,
            'intent'        : intent
        }

        self._sock.send(bytes(json.dumps(init_message), 'utf-8'))

        response = self._sock.recv(1024)

        if response == 'no joining':
            raise Exception('Cannot Join, Server Started')

    def _recv(self, content_type):
        """ Takes care of the message receiving """

        def inner(func):

            @functools.wraps(func)
            def wrapper():
                while True:
                    sock = self._sock

                    message = sock.recv(1024)

                    data = message.decode()

                    data = json.loads(data)

                    data = MessageSchema().load(data)

                    if data.content_type == content_type:
                        value = func(json.loads(data.content) if content_type == 'dict' else data.content)
                        return value

            return wrapper

        return inner

    @_recv('str')
    def recv_str(self, message):
        return message

    @_recv('dict')
    def recv_json(self, message):
        return message

    def _send(self, message, content_type):

        sock = self._sock

        message_obj = Message(
            content=message,
            content_type=content_type
        )

        data = MessageSchema().dumps(message_obj)

        sock.send(bytes(data, 'utf-8'))

    def send_str(self, message):
        self._send(message, 'str')

    def send_json(self, message):
        self._send(json.dumps(message), 'dict')
