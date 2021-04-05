# import json
from wsock.wsock import Socket

sock = Socket(True)

# sock.subscribe('abc')
# recv = sock.recv_json()
# print(type(recv), recv)

from time import sleep

sleep(5)

sock.bind('abc')
sock.send_str('Hello Guys')

# print(sock.getMsg())

# recv = sock.recv_str()
# print(type(recv), recv)
