import socket
import json
from typing import ByteString
import uuid
import asyncio
from marshmallow import Schema, fields, post_load


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


class WSock:
    def __init__(self, host: bool):

        self._host = host

        self._port = 8765

        self._sock = socket.socket()

        self._topics = []
        self._binded_topic = ''

    '''
     * Actions
    '''

    def subscribe(self, topic):
        if (topic != '' and type(topic) == str):
            self._topics.append(topic)

    def bind(self, topic):
        print(0)
    '''
     * Class Actions
    '''

    def _restart_sock(self):
        self._sock.close()

        self._sock = socket.socket()

    '''
     * Receivers
    '''

    def _recv(self, topic, content_type):

        while (True):
            self._sock.connect(('127.0.0.1', self._port))

            message = self._sock.recv(1024)

            self._restart_sock()

            data = json.loads(message)

            data = MessageSchema().load(data)

            if ((topic != '' and data.topic == topic) or (data.topic in self._topics and len(self._topics) > 0) or (len(self._topics) == 0)):
                if ((data.content_type == content_type)):
                    return data.content

    def recv_str(self, topic=''):
        return self._recv(topic, 'str')

    def recv_json(self, topic=''):
        return self._recv(topic, 'dict')

    '''
     * Senders
    '''

    # Main method to send message
    def _send(self, msg, topic, content_type):

        self._sock.bind(('127.0.0.1', self._port))

        self._sock.listen(1)

        while (True):
            client, addr = self._sock.accept()

            message = Message(
                content=msg,
                topic=topic if topic != '' else self._binded_topic,
                content_type=content_type
            )

            data = MessageSchema().dumps(message)

            client.send(bytes(data, 'utf-8'))

            self._restart_sock()

            break

    def send_str(self, msg, topic=''):
        self._send(msg, topic, 'str')

    def send_json(self, msg, topic=''):
        self._send(msg, topic, 'dict')
