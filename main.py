import json
import sys
from socket import AF_INET, SOCK_STREAM, SocketType, socket

import logic

DEFAULT_SERVER_IP = "localhost"
SERVER_PORT = 7654
USERNAME = "CHANGE_ME"
PASSWORD = "CHANGE_ME"


def main():
    if len(sys.argv) >= 2:
        server_ip = sys.argv[1]
    else:
        server_ip = DEFAULT_SERVER_IP
    sock = connect(server_ip)
    auth(sock)
    play(sock)


def connect(addr: str) -> SocketType:
    s: SocketType = socket(AF_INET, SOCK_STREAM)
    s.connect((addr, SERVER_PORT))
    return s


def send(socket: SocketType, msg):
    json_data = json.dumps(msg) + "\n"
    print(f"Sending: {json_data}")
    socket.sendall(bytes(json_data, "utf-8"))


def recv(socket: SocketType):  # Returns a json object
    print("Waiting for data from server")
    data = socket.makefile().readline()
    if data == "":
        print("Disconnected by server")
        exit(1)
    json_data = json.loads(data)
    print(f"Received: {json_data}")
    return json_data


def auth(socket: SocketType):
    send(socket, {"auth": {"username": USERNAME, "password": PASSWORD}})


def play(socket: SocketType):
    while True:
        state = recv(socket)
        if "your-turn" in state:
            move = logic.make_move(state["your-turn"])
            send(socket, {"move": move})
        elif "error" in state:
            print(f"Server reported error:\n{state['error']}")
            exit(1)


if __name__ == "__main__":
    main()
