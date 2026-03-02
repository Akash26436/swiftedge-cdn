import socket

HOST = "127.0.0.1"
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

url = input("Enter website URL (example: https://example.com): ")
client.sendall(url.encode())

data = client.recv(1000000).decode()
print("\n----- RESPONSE RECEIVED -----\n")
print(data[:1000])

client.close()
