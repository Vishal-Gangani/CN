import socket
import threading
import sys
import time

clients = []
peer_socket = None

if len(sys.argv) != 3:
    print("Usage: python server.py <MY_PORT> <PEER_PORT>")
    sys.exit()

MY_PORT = int(sys.argv[1])
PEER_PORT = int(sys.argv[2])

def broadcast(message, sender_socket=None, from_peer=False):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)
    
    if peer_socket and not from_peer:
        try:
            peer_socket.send(message)
        except:
            pass

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg: break
            broadcast(msg, client, from_peer=False)
        except:
            break
    clients.remove(client)
    client.close()

def handle_peer():
    while True:
        try:
            msg = peer_socket.recv(1024)
            if not msg: break
            broadcast(msg, from_peer=True)
        except:
            break

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', MY_PORT))
    server.listen()
    print(f"Server running on {MY_PORT}")

    global peer_socket
    while peer_socket is None:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', PEER_PORT))
            peer_socket = s
            threading.Thread(target=handle_peer).start()
        except:
            time.sleep(1)

    while True:
        client, addr = server.accept()
        clients.append(client)
        threading.Thread(target=handle_client, args=(client,)).start()

if __name__ == "__main__":
    start()