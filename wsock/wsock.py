import socket
import json
from typing import ByteString
import uuid
import asyncio
from marshmallow import Schema, fields, post_load
from threading import Timer, Lock, Thread
from _thread import *
import sys
import logging


class MessageSchema(Schema):
    content = fields.Str()
    topic = fields.Str()
    content_type = fields.Str()

    # After the schema is
    @post_load
    def make_message(self, data, **__):
        return Message(**data)()

# Message class that will be used to send messages between connections with


class Message:
    def __init__(self, content, topic, content_type):
        self.content = content
        self.topic = topic
        self.content_type = content_type

    # If the class is called as a function

    def __call__(self):

        # The parse the content
        self.content = self.parse_content()

        # And return the whole class
        return self

    # Parses the content
    def parse_content(self):
        if (self.content_type == 'str'):
            self.content = str(self.content)
            return self.content

        else:

            if (type(self.content) == str):
                self.content = json.loads(self.content)

                return self.content

            return self.content


class Server:
    def __init__(self, timeout: int = 0):

        self._clients = []
        self._clients_lock = Lock()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = '127.0.0.1'
        self._port = 8765
        self._socket_timeout = timeout

        self._sock.bind((self._host, self._port))

        self._sock.listen()

        self._threads = []
        self.thread_count = 0

        t = Thread(target=self._start_server, daemon=False)

        t.start()

    def _start_server(self):

        try:

            while (True):
                if (self._socket_timeout != 0 and len(self._clients) == 0):

                    timer = Timer(self._socket_timeout, self.stopExec)

                    timer.start()

                c, addr = self._sock.accept()

                if (self._socket_timeout != 0 and len(self._clients) == 0):
                    timer.cancel()

                self._clients.append((c, addr))

                start_new_thread(self.clientHandler, (c, addr))

                self.thread_count += 1

        except OSError as e:
            # If the error is about the running something that is not a socket, just pass because the socket was closed
            if (str(e) == '[WinError 10038] An operation was attempted on something that is not a socket'):
                pass
            else:
                print(e)

        self._sock.close()

    def stopExec(self, msg=''):
        logging.info(msg if msg != '' else 'Server timed out! No connection established under the timeout given ...')
        self._sock.close()

        sys.exit()

    def _check_clients(self, addr):
        for client, address in self._clients:
            if (address == addr):
                self._clients.remove((client, address))

        if (len(self._clients) == 0):
            self.stopExec('All clients disconnected, shutting down server ...')

    def clientHandler(self, c, addr):
        logging.info(addr, 'is connected')

        try:
            while (True):
                data = c.recv(2048)

                if not data:
                    break

                for client, address in self._clients:
                    if (client != c):
                        client.send(data)

            c.close()

            self._check_clients(addr)

            self.thread_count -= 1
            exit()

        except Exception as e:

            if (str(e) == '[WinError 10054] An existing connection was forcibly closed by the remote host'):
                self._check_clients(addr)

            else:
                print('err', e)


class WSock:
    def __init__(self):
        self.sock_name = f'Sock-{uuid.uuid4().hex[:4]}'

        self._port = 8765

        self._sock = socket.socket()
        self._sock.connect(('127.0.0.1', 8765))

        self._topics = []
        self._binded_topic = ''

    '''
     * Actions
    '''

    def subscribe(self, topic: str):
        if (topic != '' and type(topic) == str):
            self._topics.append(topic)
        elif (type(topic) != str):
            raise TypeError('Topic have to be a string')

    def bind(self, topic: str):
        if (type(topic) != str):
            raise TypeError('Topic have to be a string')

        self._binded_topic = topic

    '''
     * Class Actions
    '''

    '''
     * Receivers
    '''

    def _recv(self, topic, content_type):

        while (True):
            sock = self._sock

            message = sock.recv(1024)

            data = message.decode()

            data = json.loads(message)

            data = MessageSchema().load(data)

            if ((topic != '' and data.topic == topic) or (data.topic in self._topics and len(self._topics) > 0) or (len(self._topics) == 0)):
                if ((data.content_type == content_type)):
                    return json.loads(data.content) if content_type == dict else data.content

    def recv_str(self, topic=''):
        return self._recv(topic, 'str')

    def recv_json(self, topic=''):
        return self._recv(topic, 'dict')

    '''
     * Senders
    '''

    def _send(self, msg, topic, content_type):
        sock = self._sock

        message = Message(
            content=msg,
            topic=topic if topic != '' else self._binded_topic,
            content_type=content_type
        )

        data = MessageSchema().dumps(message)

        sock.send(bytes(data, 'utf-8'))

    def send_str(self, msg, topic=''):
        self._send(msg, topic, 'str')

    def send_json(self, msg, topic=''):
        self._send(json.dumps(msg), topic, 'dict')
