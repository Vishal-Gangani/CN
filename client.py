import socket, threading, random, sys

def receive(sock):
    while True:
        try:
            print(f"\n{sock.recv(1024).decode()}")
        except: sys.exit(0)


mode = input("Mode (M)anual / (R)ound-Robin: ").upper()
if mode == 'M':
    port = int(input("Port (8000/8001): "))
else:
    port = random.choice([8000, 8001])
    print(f"Round-Robin assigned port: {port}")

proto = input("Protocol (TCP/UDP): ").upper()
name = input("Username: ")


if proto == 'TCP':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', port))
else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('127.0.0.1', port))
    sock.send(b"__JOIN__")


threading.Thread(target=receive, args=(sock,), daemon=True).start()

while True:
    try:
        msg = input()
        sock.send(f"[{name}]: {msg}".encode())
    except: break