#!/usr/local/bin/python3

import socket
import sys
from ClientThread import ClientThread

host = '0.0.0.0'
port = 7777

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
	print('Could not create socket.')
	sys.exit(0)

print('[-] Socket Created')

try:
	s.bind((host, port))
	print('[-] Socket bound to port ' + str(port))
except:
	print('Bind failed')
	sys.exit()

s.listen(10)
print('Listening...')

while True:
	client, addr = s.accept()
	print('[-] Connected to ' + addr[0] + ':' + str(addr[1]))
	thread = ClientThread(client)
	thread.start()

s.close()
