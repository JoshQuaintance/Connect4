# import json
from wsock.wsock import Socket

sock = Socket(True)

sock.subscribe('abc')
recv = sock.recv_json()
print(type(recv), recv)

sock.unsubscribe('abc')
recv2 = sock.recv_json()
print(type(recv2), recv2)

# recv = sock.recv_str()
# print(type(recv), recv)
