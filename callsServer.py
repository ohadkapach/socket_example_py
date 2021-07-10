import socket
from threading import Thread

class CallsServer:
    def __init__(self):
        self.operation_host = "127.0.0.1"
        self.operation_port = 5003

        self.server_host = "0.0.0.0"
        self.server_port = 7000

        self.separator_token = "<SEP>"
        self.client_sockets = set()
        self.sock = None
        self.operation_socket = None

        self.connect_to_operation_server()

        self.create_tcp_socket()
        if self.sock:
            self.run_connection_listener()

    def listen_for_operations(self):
        while True:
            message = self.operation_socket.recv(1024).decode()
            print("\n" + message)

    def connect_to_operation_server(self):
        self.operation_socket = socket.socket()
        print(f"[*] Connecting to {self.operation_host}:{self.operation_port}...")
        self.operation_socket.connect((self.operation_host, self.operation_port))
        print("[+] Connected.")
        t = Thread(target=self.listen_for_operations)
        t.daemon = True
        t.start()

    def create_tcp_socket(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.server_host, self.server_port))
        self.sock.listen(5)
        print(f"[*] Listening as {self.server_host}:{self.server_port}")

    def listen_for_client(self, cs):
        """
        This function keep listening for a message from `cs` socket
        Whenever a message is received, broadcast it to all other connected clients
        """
        while True:
            try:
                msg = cs.recv(1024).decode()
            except Exception as e:
                print(f"[!] Error: {e}")
                self.client_sockets.remove(cs)
            else:
                if self.separator_token in msg:
                    msg = msg.split(self.separator_token)
                    if msg[0] == "ohad" and int(msg[1]) == 123:
                        pass
                elif msg == "get devices":
                        self.operation_socket.send(msg.encode())
                else:
                    print(msg)

                    # self.open_devices_server(cs)
                    # # # iterate over all connected sockets
                    #     for client_socket in client_sockets:
                    #         # and send the message
                    #         client_socket.send(msg.encode())
                    #

    def run_connection_listener(self):
        while True:
            client_socket, client_address = self.sock.accept()
            print(f"[+] {client_address} connected.")
            self.client_sockets.add(client_socket)
            t = Thread(target=self.listen_for_client, args=(client_socket,))
            t.daemon = True
            t.start()

        # # close client sockets
        # print("here closed")
        # for cs in self.client_sockets:
        #     cs.close()
        # # close server socket
        # self.sock.close()


obj = CallsServer()






