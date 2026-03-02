import socket

HOST = "0.0.0.0"
PORT = 8000

EDGE_SERVERS = [
    ("127.0.0.1", 9001),
    ("127.0.0.1", 9002)
]

current = 0

def get_next_server():
    global current
    server = EDGE_SERVERS[current]
    current = (current + 1) % len(EDGE_SERVERS)
    return server

def handle_client(client_conn):
    url = client_conn.recv(4096)

    edge_host, edge_port = get_next_server()
    print(f"Routing request to Edge Server {edge_port}")

    edge_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    edge_socket.connect((edge_host, edge_port))
    edge_socket.sendall(url)

    response = edge_socket.recv(1000000)

    client_conn.sendall(response)

    edge_socket.close()
    client_conn.close()

def start_load_balancer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Load Balancer running on port {PORT}...")

    while True:
        client_conn, addr = server.accept()
        handle_client(client_conn)

if __name__ == "__main__":
    start_load_balancer()
