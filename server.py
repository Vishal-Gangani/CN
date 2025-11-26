import socket, threading, sys, time

MY_PORT = int(sys.argv[1])
PEER_PORT = int(sys.argv[2])

tcp_clients, udp_clients = [], set()
peer_sock = None


udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('0.0.0.0', MY_PORT))

def broadcast(msg, sender_sock=None, sender_addr=None):
    
    for client in tcp_clients:
        if client != sender_sock:
            try: client.send(msg)
            except: tcp_clients.remove(client)
    
    for addr in udp_clients:
        if addr != sender_addr:
            udp_sock.sendto(msg, addr)

def handle_tcp(conn):
    tcp_clients.append(conn)
    while True:
        try:
            msg = conn.recv(1024)
            if not msg: break
            broadcast(msg, sender_sock=conn)
            if peer_sock: peer_sock.send(b'FWD:' + msg)
        except: break
    conn.close()

def handle_udp():
    while True:
        msg, addr = udp_sock.recvfrom(1024)
        if addr not in udp_clients: udp_clients.add(addr)
        if msg == b"__JOIN__": continue 
        
        broadcast(msg, sender_addr=addr)
        if peer_sock: peer_sock.send(b'FWD:' + msg)

def handle_peer():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', MY_PORT + 100))
    s.listen(1)
    conn, _ = s.accept()
    while True:
        try:
            msg = conn.recv(1024)
            if not msg: break
            if msg.startswith(b'FWD:'):
                broadcast(msg[4:])
        except: break

def connect_peer():
    global peer_sock
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', PEER_PORT + 100))
            peer_sock = s
            break
        except: time.sleep(1)


threading.Thread(target=handle_udp, daemon=True).start()
threading.Thread(target=handle_peer, daemon=True).start()
threading.Thread(target=connect_peer, daemon=True).start()


tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(('0.0.0.0', MY_PORT))
tcp_server.listen()
print(f"Server running on {MY_PORT}")

while True:
    conn, _ = tcp_server.accept()
    threading.Thread(target=handle_tcp, args=(conn,), daemon=True).start()