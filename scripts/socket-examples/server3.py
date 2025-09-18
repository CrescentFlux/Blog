import socket
import os
import threading
print("当前用户",os.getlogin())
print("当前工作目录",os.getcwd())
print("/tmp权限",oct(os.stat("/tmp").st_mode)[-3:])
# 创建 Unix Socket
server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
socket_path = "/tmp/my_socket"

# 清理可能存在的旧socket文件
if os.path.exists(socket_path):
    os.remove(socket_path)

server_socket.bind(socket_path)
server_socket.listen(1)
print("服务器已经启动等待连接 ")

# 接受连接（修复变量名）
connection, client_address = server_socket.accept()
print('客户端已连接')

def receive_message():
    """接收消息的线程函数"""
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                print("客户端断开连接")
                break
            message = data.decode('utf-8')
            print(f'客户端说: {message}')
    except:
        print("接受消息出错")

def send_message():
    """发送消息的线程函数"""
    try:
        while True:
            message = input("服务端输入消息: ")
            connection.send(message.encode('utf-8'))
    except:
        print("发送消息出错")

# 创建并启动线程
recv_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

recv_thread.start()
send_thread.start()

# 等待线程结束
recv_thread.join()
send_thread.join()

connection.close()
server_socket.close()
os.remove(socket_path)
print('服务器已关闭')