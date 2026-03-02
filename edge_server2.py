import socket
import requests
import os
import hashlib

HOST = "0.0.0.0"
PORT = 9002
CACHE_DIR = "cache"

# Create cache folder if not exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_cache_filename(url):
    return os.path.join(CACHE_DIR, hashlib.md5(url.encode()).hexdigest())

def fetch_from_origin(url):
    try:
        response = requests.get(url)
        return response.text
    except:
        return "Error fetching page."

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")

    try:
        url = conn.recv(4096).decode().strip()
        print(f"Requested URL: {url}")

        cache_file = get_cache_filename(url)

        if os.path.exists(cache_file):
            print("CACHE HIT")
            with open(cache_file, "r", encoding="utf-8") as f:
                data = f.read()
        else:
            print("CACHE MISS - Fetching from origin server")
            data = fetch_from_origin(url)
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(data)

        conn.sendall(data.encode())

    except Exception as e:
        print("Error:", e)

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Edge Server running on port {PORT}...")

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)

if __name__ == "__main__":
    start_server()
