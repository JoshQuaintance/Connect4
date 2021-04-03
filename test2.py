from wsock.wsock import Socket

sock = Socket(False)

sock.bind('abc')
sock.send_json({'message': 'hello', 'data': [1, 2, 3, 4, 5]})
