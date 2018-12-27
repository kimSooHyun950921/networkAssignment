import ssl
import socket

hostname = 'localhost'
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

with socket.create_connection((hostname,5000)) as sock:
    with context.wrap_socket(sock,server_hostname=hostname) as ssock:
        ssock.send("hi".encode())
        print(ssock.recv(1024()).decode())
