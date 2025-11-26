import socket
import threading

def receive(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print(msg)
        except:
            sock.close()
            break

def start():
    port = int(input("Connect to Server Port (8000 or 8001): "))
    name = input("Username: ")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', port))
    
    threading.Thread(target=receive, args=(client,)).start()
    
    while True:
        msg = input()
        client.send(f"{name}: {msg}".encode())

if __name__ == "__main__":
    start()