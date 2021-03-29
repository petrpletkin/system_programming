import sys
from os import getenv
from socket import AF_INET, SOCK_STREAM, socket, SOCK_DGRAM
from typing import Tuple
from util import SOCK_TYPE_NAME


class DifferentSocketConnector:

    def __init__(self, address:  Tuple[int, int], socket_type: int = SOCK_STREAM):
        self._socket_type = socket_type
        self._addr = address
        self._socket_instance: socket = None
        self._setup_sock_connection()

    def _setup_sock_connection(self):
        self._socket_instance = socket(AF_INET, self._socket_type)
        if self._socket_type == SOCK_STREAM:
            self._socket_instance.connect(self._addr)

    def send_message(self, sock_message: str):
        if self._socket_type == SOCK_DGRAM:
            self._send_to_udp(sock_message.encode())
        elif self._socket_type == SOCK_STREAM:
            self._send_to_tcp(sock_message.encode())

    def _send_to_udp(self, sock_message: bytes):
        self._socket_instance.sendto(sock_message, self._addr)

    def _send_to_tcp(self, sock_message: bytes):
        self._socket_instance.send(sock_message)

    def recv_message(self):
        data = self._socket_instance.recv(1024)
        print(f"Received from {SOCK_TYPE_NAME[self._socket_type]}: {data.decode()}")


if __name__ == '__main__':
    client_sock_type = int(sys.argv[1]) if len(sys.argv) > 1 else SOCK_STREAM

    addr = (getenv("SOCK_SERVER_HOST", "localhost"), int(getenv("SOCK_SERVER_PORT", 5555)))
    client = DifferentSocketConnector(addr, client_sock_type)
    client.send_message(f"Hello from {SOCK_TYPE_NAME[client_sock_type]} client!")
    client.recv_message()
