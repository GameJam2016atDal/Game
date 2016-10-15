#!/usr/bin/python

import socket
import sys
from thread import start_new_thread

HOST = 'localhost' # all availabe interfaces
PORT = 7777 # arbitrary non privileged port 

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
    print("Could not create socket. Error Code: ")
    sys.exit(0)

print("[-] Socket Created")

# bind socket
try:
    s.bind((HOST, PORT))
    print("[-] Socket Bound to port " + str(PORT))
except:
    print("Bind Failed. Error Code:")
    sys.exit()

s.listen(10)
print("Listening...")

def client_thread(conn):
    conn.send("Welcome to the Server. Type messages and press enter to send.\n")

    while True:
        data = conn.recv(10).strip()
        if not data:
            break
        print(data)
        reply = "OK . . " + data
        conn.send(reply)
    conn.close()

while True:
    # blocking call, waits to accept a connection
    conn, addr = s.accept()
    print("[-] Connected to " + addr[0] + ":" + str(addr[1]))

    start_new_thread(client_thread, (conn,))

s.close()
