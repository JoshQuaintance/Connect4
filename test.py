from wsock.wsock import WSock
from time import sleep

s = WSock(True)

# s.send_str({'message': 'hello'})

print(s.recv_str())



# s.send_str('close-server')

# print(s.recv_json())
