import socket
from threading import Thread


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7000 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

user_name = input("Enter your User Name: ")
user_pass = input("Enter your Password: ")
login_dict = {user_name: user_pass}
data = user_name + separator_token + str(user_pass)
s.send(data.encode())


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()


while True:
    to_send =  input()
    if to_send.lower() == 'q':
        break
    s.send(to_send.encode())

s.close()


