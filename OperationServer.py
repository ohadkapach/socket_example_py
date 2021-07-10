import socket
from threading import Thread


class OperationServer:
    def __init__(self):
        self.server_host = "0.0.0.0"
        self.server_port = 5003
        self.separator_token = "<SEP>"
        self.client_sockets = set()
        self.sock = None
        self.devices = ['camera', 'micro', 'tv', 'mobile']
        self.create_tcp_socket()
        if self.sock:
            self.run_connection_listener()

    def create_tcp_socket(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.server_host, self.server_port))
        self.sock.listen(5)
        print(f"[*] Listening as {self.server_host}:{self.server_port}")

    def listen_for_client(self, cs):
        while True:
            try:
                print("here")
                msg = cs.recv(1024).decode()
                if msg.lower() == "get devices":
                    print("here", self.client_sockets)
                    for client_socket in self.client_sockets:
                        print(client_socket)
                        # and send the message
                        client_socket.send(str(self.devices).encode())
                        # self.sock.send(str(self.devices).encode())
            except Exception as e:
                print(f"[!] Error: {e}")
                self.client_sockets.remove(cs)
            else:
                print(msg)

    def run_connection_listener(self):
        while True:
            client_socket, client_address = self.sock.accept()
            print(f"[+] {client_address} connected.")
            self.client_sockets.add(client_socket)
            t = Thread(target=self.listen_for_client, args=(client_socket,))
            t.daemon = True
            t.start()

        # # close client sockets
        # for cs in self.client_sockets:
        #     cs.close()
        # # close server socket
        # self.sock.close()


obj = OperationServer()






