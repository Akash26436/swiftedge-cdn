import time

RATE_LIMIT = 5
WINDOW = 10
BLOCK_TIME = 20

request_log = {}
blocked_ips = {}
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

def handle_client(client_conn, addr):
    client_ip = addr[0]
    current_time = time.time()

    # Check if IP is blocked
    if client_ip in blocked_ips:
        if current_time < blocked_ips[client_ip]:
            print(f"Blocked IP {client_ip}")
            client_conn.sendall(b"Too many requests. Try later.")
            client_conn.close()
            return
        else:
            del blocked_ips[client_ip]

    # Initialize request log
    if client_ip not in request_log:
        request_log[client_ip] = []

    # Remove old timestamps
    request_log[client_ip] = [
        t for t in request_log[client_ip]
        if current_time - t < WINDOW
    ]

    request_log[client_ip].append(current_time)

    # Check rate limit
    if len(request_log[client_ip]) > RATE_LIMIT:
        blocked_ips[client_ip] = current_time + BLOCK_TIME
        print(f"Rate limit exceeded for {client_ip}")
        client_conn.sendall(b"Rate limit exceeded.")
        client_conn.close()
        return

    # Continue normal routing
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
        handle_client(client_conn, addr)

if __name__ == "__main__":
    start_load_balancer()
