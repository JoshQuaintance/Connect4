# from wsock.wsock import Server

# s = Server(timeout=1)
from time import sleep
import sys

for i in range(20):
    
    print(f'\r{str(i)}', end="")
    sleep(1)
    sys.stdout.flush()

# from wsock.wsock import WSock
# from time import sleep

# s = WSock()

# # s.send_str({'message': 'hello'})

# s.subscribe('abc')

# print(s.recv_str())

# s.send_str('close-server')

# print(s.recv_json())
