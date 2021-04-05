from wsock.wsock import WSock

s = WSock(True)

s.send_str('hello')

print(s.recv_str())