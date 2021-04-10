import socket
import json
import uuid
from marshmallow import Schema, fields, post_load
from threading import Timer, Lock, Thread
import os
import logging


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


class Server:
    def __init__(self, timeout: int = 0):

        # Socket initializations
        self._clients = []
        self._clients_lock = Lock()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = '127.0.0.1'
        self._port = 8765
        self._socket_timeout = timeout

        # Set socket to be able to re-use an address if it wasn't closed
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Set socket to be able to re-use a port/address of an active socket
        # This is important so that if one host turns off, other clients won't turn off
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        # Binds the socket into an address
        self._sock.bind((self._host, self._port))

        # Listen to as many socket as possible
        self._sock.listen()

        # Create a thread to start the server
        t = Thread(target=self._start_server, daemon=False)

        # Start the thread
        t.start()

    def _start_server(self):
        ''' Method to start the server '''

        import threading

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
                t = threading.Thread(target=self.clientHandler, args=(c, addr), daemon=True).start()

        except OSError as e:

            # If the error is about the running something that is not a socket, just pass because the socket was closed
            if (str(e) == '[WinError 10038] An operation was attempted on something that is not a socket'):
                pass
            else:
                print(e)

        self._sock.close()

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
        # print(addr, 'is connected')

        try:

            # Loop infinitely
            while (True):

                # Get data from the client
                data = c.recv(2048)

                # If the data is empty, then break
                if not data:
                    break


                # Loop through every client in the list
                for client, address in self._clients:

                    # If the client is not the same as the client the message is received from
                    if (client != c):

                        # Send the data to the client
                        client.send(data)
            
            self._check_clients(addr)

            exit()

        except Exception as e:

            if (str(e) == '[WinError 10054] An existing connection was forcibly closed by the remote host'):
                self._check_clients(addr)

            else:
                print('err', e)


class WSock:
    ''' Websocket implementation that have Publisher and Subscribers as it's main target '''

    def __init__(self):

        # Create a unique socket name
        self.sock_name = f'Sock-{uuid.uuid4().hex[:4]}'

        # Socket init
        self._port = 8765

        self._sock = socket.socket()
        self._sock.connect(('127.0.0.1', 8765))

        self._topics = []
        self._binded_topic = ''

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
            data = json.loads(message)

            # Deserialize it using marshmallow
            data = MessageSchema().load(data)

            
            if (
                (topic != '' and data.topic == topic) or 
                (data.topic in self._topics and len(self._topics) > 0) or 
                (len(self._topics) == 0)
            ):
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
