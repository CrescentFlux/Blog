##使用TCP socket代替unix socket
import socket
import threading

def handle_client(connection, address):
    """处理单个客户端连接的线程函数"""
    print(f"客户端 {address} 已连接")
    
    try:
        while True:
            # 接收客户端消息
            data = connection.recv(1024)
            if not data:
                print(f"客户端 {address} 断开连接")
                break
                
            message = data.decode('utf-8')
            print(f"客户端{address}说: {message}")
            
            # 回复客户端
            reply = input(f"回复给{address}: ") or f"服务器收到: {message}"
            connection.send(reply.encode('utf-8'))
            
    except Exception as e:
        print(f"与客户端 {address} 通信出错: {e}")
    finally:
        connection.close()

# 创建TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 设置地址重用，避免"Address already in use"错误
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定地址和端口
host = '127.0.0.1'  # 本地回环地址，只允许本机连接
port = 12345        # 端口号（1024-65535之间的任意数字）
server_socket.bind((host, port))

# 开始监听，允许最多5个客户端排队
server_socket.listen(5)
print(f"服务器启动在 {host}:{port}，等待客户端连接...")

try:
    while True:
        # 接受客户端连接
        connection, address = server_socket.accept()
        
        # 为每个客户端创建新线程
        client_thread = threading.Thread(target=handle_client, args=(connection, address))
        client_thread.daemon = True  # 设置守护线程
        client_thread.start()
        
except KeyboardInterrupt:
    print("\n服务器正在关闭...")
finally:
    server_socket.close()