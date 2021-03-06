import socket
import json
from time import sleep
import uuid
from marshmallow import Schema, fields, post_load
from threading import Timer, Lock, Thread
import os
import logging
from types import SimpleNamespace


class MessageSchema(Schema):
    ''' Message Schema for serializing and deserializing messages between sockets '''

    # Content of the message will be a string
    content = fields.Str()

    # Same as contemt
    topic = fields.Str()

    # Same as above
    content_type = fields.Str()

    # After the schema is loaded (MessageSchema().loads(dict))
    @post_load
    def make_message(self, data, **__):
        # It will pass all it's data into the Message object to
        # make it a Message object again
        return Message(**data)()


class Message:
    ''' Message class that will be used to send messages between connections with '''

    def __init__(self, content, topic, content_type):

        # Initializations
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


class StoreServer:
    def __init__(self):
        # self._sock = WSock(8766)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._store_server_name = 'Store-Sock-' + str(uuid.uuid4().hex[:4])

        self._sock.bind(('127.0.0.1', 8766))
        self._sock.listen()

        self._servers_active: set = set()
        self._validation_queue = []


        self._sync_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sync_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sync_sock.bind(('127.0.0.1', 8767))
        self._sync_sock.listen()

        Thread(target=self._server_sync, daemon=True).start()


        Thread(target=self._client_handler, daemon=True, name='StoreServer._client_handler()').start()
        Thread(target=self._token_validator, daemon=True, name='StoreServer._token_handler()').start()

        Thread(target=self.tt, daemon=True).start()

    def tt(self):
        while (True):
            print(self._servers_active)
            sleep(5)

    def _server_sync(self):
        while (True):
            sock = self._sync_sock
            
            c, addr = sock.accept()

            data = c.recv(1024).decode()

            data = json.loads(data)

            self._servers_active = self._servers_active.union(set(data['servers']))

    def _client_handler(self):
        while (True):
            sock = self._sock

            c, addr = sock.accept()
            
            data = c.recv(1024).decode()

            data = MessageSchema().loads(data)

            print(type(data.content), data.content)
            
            data = SimpleNamespace(**json.loads(data.content))

            print(data.action)

            if (data.action == 'update-server-list'):
                self._servers_active = self._servers_active.union(set(data.servers))

            if (data.action == 'new-server'):
                self._servers_active.add(data.topic)

                message = json.dumps({
                    'action': 'update-server-list',
                    'servers': list(self._servers_active)
                })

                self._sync_sock.connect(('127.0.0.1', 8767))
                self._sync_sock.send(bytes(message, 'utf-8'))

            elif (data.action == 'validate-token'):
                queue = {
                    'token': data.topic,
                    'private_token': data.private_token
                }

                self._validation_queue.append(queue)

    def _token_validator(self):
        while (True):
            if (len(self._validation_queue) == 0):
                continue

            token = self._validation_queue[0]
            private_token = token['private_token']
            token = token['token']

            available_tokens = self._servers_active
            sock = self._sock

            if (token not in available_tokens):
                message = Message(
                    content=json.dumps({
                        'response': 'token-non-existent',
                        'private_token': private_token
                    }),
                    content_type='dict',
                    topic=''
                )

                message = bytes(MessageSchema().dumps(message), 'utf-8')

                sock.send_json(message)

            if (token in available_tokens):
                message = Message(
                    content=json.dumps({
                        'response': 'token-exist',
                        'private_token': private_token
                    }),
                    content_type='dict',
                    topic=''
                )

                message = bytes(MessageSchema().dumps(message), 'utf-8')

                sock.send_json(message)

            del self._validation_queue[0]


class Server:
    def __init__(self, timeout: int = 0, server_token=''):

        # Socket initializations
        self._clients: list[(socket.socket, socket._RetAddress)] = []
        self._clients_lock = Lock()
        self._message_queue = []
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = '127.0.0.1'
        self._port = 8765
        self._socket_timeout = timeout

        # Set socket to be able to re-use an address if it wasn't closed
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Set socket to be able to re-use a port/address of an active socket
        # This is important so that if one host turns off, other clients won't turn off
        if os.name != 'nt':
            self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Binds the socket into an address
        self._sock.bind((self._host, self._port))

        # Listen to as many socket as possible
        self._sock.listen()

        # Create a thread to start the server
        Thread(target=self._start_server, daemon=True).start()
        Thread(target=self._sender_handler, daemon=True).start()

        token_validator = StoreServer()

        tkn_check = Message(
            content=json.dumps({
                'action': 'new-server',
                'topic': server_token
            }),
            topic='',
            content_type='dict'
        )

        tkn_check = MessageSchema().dumps(tkn_check)

        store_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        store_sock.connect(('127.0.0.1', 8766))

        store_sock.send(bytes(tkn_check, 'utf-8'))


    def _sender_handler(self):

        while (True):
            if (len(self._message_queue) == 0):
                continue

            sender_addr, msg = self._message_queue[0]

            for client, address in self._clients:
                if (address != sender_addr):
                    try:
                        client.sendall(msg)

                    except Exception as e:

                        if (str(e) == '[WinError 10054] An existing connection was forcibly closed by the remote host' or
                                str(e) == '[WinError 10053] An established connection was aborted by the software in your host machine'):
                            self._check_clients(address)

                        else:
                            print(e)

            del self._message_queue[0]

    def _start_server(self):
        ''' Method to start the server '''

        from threading import Timer, Thread

        try:

            # Infinitely loop
            while (True):

                # If there is a timeout, and the there is no clients connected
                # If the cancel didn't run (meaning nobody connected within the timeout time),
                # then it will stop the server
                if (self._socket_timeout != 0 and len(self._clients) == 0):

                    # Create a timer thread
                    timer = Timer(self._socket_timeout, self.stopExec)

                    # start it
                    timer.start()

                # Wait and accept an incoming connection (blocking)
                c, addr = self._sock.accept()

                # If there is a timeout, and the there is no clients connected
                if (self._socket_timeout != 0 and len(self._clients) == 0):

                    # Cancel the timeout
                    timer.cancel()

                # Append the client and address into the list of clients
                self._clients.append((c, addr))

                # Start a new thread to handle client messages
                Thread(target=self.clientHandler, args=(c, addr), daemon=True).start()

        except OSError as e:

            # If the error is about the running something that is not a socket, just pass because the socket was closed
            if (str(e) == '[WinError 10038] An operation was attempted on something that is not a socket'):
                pass
            else:
                print(e)

    def stopExec(self, msg=''):
        ''' Method to shutdown the server if needed '''

        logging.info(msg if msg != '' else 'Server timed out! No connection established under the timeout given ...')
        print(msg if msg != '' else 'Server timed out! No connection established under the timeout given ...')

        # Exit with 0 code
        os._exit(0)

    def _check_clients(self, addr):
        ''' Method to check if client exist and to remove if necessary '''

        # Loop through all the clients
        for client, address in self._clients:

            # If the address from the clients list is the same from the given address
            if (address == addr):

                # Remove the client from the clients list
                self._clients.remove((client, address))

                break

        # If the clients list is empty
        if (len(self._clients) == 0):

            # Stop the server
            self.stopExec('All clients disconnected, shutting down server ...')

    def clientHandler(self, c, addr):
        ''' Handles client messages (receives messages and will send it back to other clients, basically a router) '''

        logging.info(addr, 'is connected')
        try:

            # Loop infinitely
            while (True):

                # Get data from the client
                data = c.recv(2048)

                # If the data is empty, then break
                if not data:
                    continue

                self._message_queue.append((addr, data))

        except Exception as e:

            if (str(e) == '[WinError 10054] An existing connection was forcibly closed by the remote host' or
                    str(e) == '[WinError 10053] An established connection was aborted by the software in your host machine'):
                self._check_clients(addr)

            else:
                print('err', e)


class WSock:
    ''' Websocket implementation that have Publisher and Subscribers as it's main target '''

    def __init__(self, port=None):

        # Create a unique socket name
        self.sock_name = f'Sock-{uuid.uuid4().hex[:4]}'

        # Socket init
        self._port = port if port != None else 8765

        self._sock = socket.socket()
        self._sock.connect(('127.0.0.1', self._port))

        self._topics = []
        self._binded_topic = ''

    def getSock(self):
        return self._sock

    '''
     * Actions
    '''

    def subscribe(self, topic: str):
        ''' Subscribes the current socket to a specific topic (For sending to a specific topic) '''

        if (topic != '' and type(topic) == str):
            self._topics.append(topic)
        elif (type(topic) != str):
            raise TypeError('Topic have to be a string')

    def bind(self, topic: str):
        ''' Binds the current socket to a specific topic (For receiving from specific topics) '''

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
        ''' Handles the socket's message receiving '''

        # Loop infinitely
        while (True):

            # Create a local variable to the socket
            sock = self._sock

            # Receive a message
            message = sock.recv(1024)

            # Decode it from bytes into string
            data = message.decode()

            # Load it as a dict
            data = json.loads(data)

            # Deserialize it using marshmallow
            data = MessageSchema().load(data)

            if (
                (topic != '' and data.topic == topic) or
                (data.topic in self._topics and len(self._topics) > 0) or
                (len(self._topics) == 0)
            ):
                if ((data.content_type == content_type)):
                    return SimpleNamespace(**json.loads(data.content)) if content_type == 'dict' else data.content

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
        # if (type(msg) == SimpleNamespace()):
        #     msg = vars(SimpleNamespace)

        self._send(json.dumps(msg), topic, 'dict')
