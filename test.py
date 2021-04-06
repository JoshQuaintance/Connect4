from wsock.wsock import WSock

s = WSock(True)

s.send_json({'message': 'hello'})

s.send_str('close-server')

# print(s.recv_json())
