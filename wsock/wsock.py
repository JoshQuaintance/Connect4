import websockets
import json
import asyncio
import uuid
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



class Socket:

    def __init__(self, host: bool):

        self.host = host

        self.topics = []
        self.binded_topic = None
        self.use_topic = False

        if (self.host):
            self.topic = uuid.uuid4().hex[:6]
            self._serve()


        self._message = None
        self._message_type_expected = None
        self._recv_type = None


    '''
     * Action Methods
    '''
    
    def subscribe(self, topic):
        ''' Methods to subscribe to specific topic '''

        # If the topic was just an empty string
        if (topic != '' and type(topic) == str):
            self.topics.append(topic)
            self.use_topic = True
        else:
            self.use_topic = False

    def unsubscribe(self, *topics):
        ''' Method to unsubscribe a listener from a topic '''

        # If there is only 1 topic given and it is empty string
        if (len(topics) == 1 and topics[0] == ''):

            # Clear the topic
            self.topics = [] 

            self.use_topic = False

            return

        for topic in topics:

            # If the topic given is a subscribed topic
            if topic in self.topics:

                # Delete the topic
                self.topics.remove(topic)

            # If it doesn't exist
            else:
                
                # raise a ValueError 
                raise ValueError(f"Socket.unsubscribe(*topics): '{topic}' is not a subscribed topic")

        if (len(topics) == 0):
            self.use_topics = False

    def bind(self, topic):
        ''' Method to bind a sender to a specific topic '''

        if (topic == ''):

            # Clears the bind
            self.binded_topic = None

        elif (type(topic) == str):
            
            # Sets the binded topic
            self.binded_topic = topic

        else:
            raise Error('Topic has to be a string')


    '''
     * Class Action Methods
    '''

    async def _close_sock(self, websocket):
        try:
            await websocket.close()

        except websockets.exceptions.ConnectionClosedOK as e:
            print('OK')

    def _serve(self):
        ''' Serves ( starts ) the websocket server 
            
            Only used for host only
        '''
        start_receiver = websockets.serve(self._recv, 'localhost', 8765)

        asyncio.get_event_loop().run_until_complete(start_receiver)


    '''
     * Listeners
    '''

    async def _recv(self, websocket, path):
        
        # Get the data and load the json into a dict
        data = json.loads(await websocket.recv())

        # Load the dict back into a Message object
        data = MessageSchema().load(data)


        print('cont: ', data.content)
        print('topic: ', data.topic)
        print('use: ', self.use_topic)
        print('topics: ', self.topics)
        print('cont_type: ', data.content_type)
        print('expected: ', self._message_type_expected)
        # Check to use topic or not if we do, check if the topic is similar
        # If we don't use topic, then just run it
        if (self.use_topic and data.topic in self.topics or self.use_topic == False):

            # If the content type is not what is expected
            if (data.content_type != self._message_type_expected):
                
                await self._close_sock(websocket)

                # Ignore the message
                return
            
            # Get the current running loop
            loop = asyncio.get_running_loop()

            # Make the _message into the content of the message
            self._message = json.loads(data.content) if data.content_type == dict else data.content

            print(self._message)
            print()

            await websocket.close()
            # await self._close_sock(websocket)

            # End the loop 
            loop.stop()

        else:
            await self._close_sock(websocket)


    '''
     * Senders
    '''

    async def _send(self, topic, msg):
        async with websockets.connect('ws://localhost:8765') as websocket:
            
            print(type(msg), msg)

            # Create a message object 
            message = Message(
                content = msg,
                topic = topic if topic != '' and type(topic) == str else self.binded_topic or '',
                content_type = self._message_type_expected,
            )

            # Dump the data ( serialize it )
            data = MessageSchema().dumps(message)

            # Dump it into stringified json then send it
            await websocket.send(data)

    '''
     *  Callers
    '''

    def send_str(self, msg, topic = ''):
        
        self._message_type_expected = 'str'
        asyncio.get_event_loop().run_until_complete(self._send(topic, msg))

    def send_json(self, json_data, topic = ''):

        self._message_type_expected = 'dict'
        asyncio.get_event_loop().run_until_complete(self._send(topic, json.dumps(json_data)))


    def recv_str(self):

        self._message_type_expected = 'str'

        asyncio.get_event_loop().run_forever()
        
        # Return the message
        return self._message

    def recv_json(self):

        self._message_type_expected = 'dict'

        asyncio.get_event_loop().run_forever()

        print('recv: ', self._message)
        
        # Return the message
        return self._message