from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from typing import Tuple
from threading import Thread


class DifferentSocketServer:
    def __init__(self, addr: Tuple[int, int], sock_type: int):
        self.socket_type = sock_type
        self.addr = addr
        self._socket = None

    def _listen_udp(self):
        while 1:
            print("Wait any connection to UDP..")
            data, addr = self._socket.recvfrom(1024)
            print(f"Received from {addr}: {data.decode()}")
            self._socket.sendto(f"Hello from UDP server!".encode(), addr)

    def _listen_tcp(self):
        self._socket.listen()
        while 1:
            print("Wait any connection to TCP..")
            connection, addr = self._socket.accept()
            with connection:
                print(f"Connected by: {addr}")
                while True:
                    data = connection.recv(1024)
                    if not data:
                        print(f"Connection from {addr} closed")
                        break
                    print(f"Received from {addr}: {data.decode()}")
                    connection.send(f"Hello from TCP server!".encode())

    def start_to_listen(self):
        with socket(AF_INET, self.socket_type) as socket_instance:
            self._socket = socket_instance
            self._socket.bind(self.addr)
            if self.socket_type == SOCK_DGRAM:
                self._listen_udp()
            elif self.socket_type == SOCK_STREAM:
                self._listen_tcp()


if __name__ == '__main__':
    tcp_server = DifferentSocketServer(('0.0.0.0', 5555), SOCK_STREAM)
    udp_server = DifferentSocketServer(('0.0.0.0', 5557), SOCK_DGRAM)
    
    tcp_thread = Thread(target=tcp_server.start_to_listen)
    tcp_thread.start()
    udp_thread = Thread(target=udp_server.start_to_listen)
    udp_thread.start()
