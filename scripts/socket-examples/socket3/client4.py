import socket
import threading

def receive_messages(client_socket):
    """接收消息的线程函数"""
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print("服务器断开连接")
                break
            message = data.decode('utf-8')
            print(f"\n服务器说: {message}")
            print("输入消息: ", end="", flush=True)
    except Exception as e:
        print(f"接收消息出错: {e}")

# 创建TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 服务器地址和端口
server_host = '127.0.0.1'  # 如果是远程服务器，改成实际IP
server_port = 12345

try:
    # 连接服务器
    client_socket.connect((server_host, server_port))
    print(f"已连接到服务器 {server_host}:{server_port}")
    print("输入消息开始聊天吧！")
    
    # 启动接收消息线程
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    recv_thread.daemon = True
    recv_thread.start()
    
    # 主线程发送消息
    while True:
        message = input("输入消息: ")
        if message.lower() == 'exit':
            break
        client_socket.send(message.encode('utf-8'))
        
except ConnectionRefusedError:
    print("连接被拒绝！请检查服务器是否启动")
except Exception as e:
    print(f"连接失败: {e}")
finally:
    client_socket.close()

