from wsock.wsock import WSock
from time import sleep

s = WSock()

s.bind('abc')

s.send_str('hello')


# print(s.recv_str())
# sock.send_str('Hello too')
