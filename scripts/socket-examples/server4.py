##使用TCP socket代替unix socket
import socket
import threading
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "127.0.0.1"
port = 12345
server_socket.bind((host,port))
server_socket.listen(1)
print(f" 服务器启动在{host}:{port}")