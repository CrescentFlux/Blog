import threading
import socket
import os


client_socket = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
socket_path= "/tmp/my_socket"
if not os.path.exists(socket_path):
    print("错误，服务端未启动！")
    print("请先运行服务端程序，然后再运行客户端")
    exit()

try:
    client_socket.connect(socket_path)
    print("已经连接到服务器")

except:
    print("无法连接到服务器")
    exit()

def receive_messages():
    #接受消息线程函数
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(" 服务端断开连接")
                break
            message = data.decode('utf-8')
            print(f'服务端说:{message}')
            print("输入消息",end="",flush=True)

    except:
        print("接收消息出错")


def send_messages():
    #发送消息的线程函数
    try:
        while True:
            message = input("输入消息：")
            client_socket.send(message.encode('utf-8'))

    except:
        print("发送消息出错")

#创建并且启动线程
recv_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)
recv_thread.start()
send_thread.start()
#等待线程结束
recv_thread.join()
send_thread.join()

client_socket.close()