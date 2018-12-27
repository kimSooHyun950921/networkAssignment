import ssl
import socket

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.load_cert_chain("server.crt","server.key")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('127.0.0.1', 2000))
    sock.listen(5)

    with context.wrap_socket(sock,server_side = True) as ssock:
        conn, addr = ssock.accept()
        print(conn.recv(1024).decode())
        conn.send("bye".encode())
