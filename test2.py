import socket
import pickle
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('127.0.0.1', 8765))

def hello():
    while (True):
        print('hello world')
    
    return 'x'

def func():
    t = threading.Thread(target=hello, daemon=True)

    t.start()

    d = pickle.dumps(t)

    print(d)

    x = pickle.loads(d)

    print(x)

func()
# s.send()


# from wsock.wsock import WSock
# from time import sleep

# s = WSock()

# s.bind('abc')

# s.send_str('hello')


# print(s.recv_str())
# sock.send_str('Hello too')
