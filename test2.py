from wsock.wsock import WSock

sock = WSock(False)

print(sock.recv_str())

sock.send_str('Hello too')