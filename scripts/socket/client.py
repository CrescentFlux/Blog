import socket
#和服务器类型相同的socket对象
client_socket = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
#指定要连接的服务器地址
socket_path = '/tmp/my_python_socket'


try:
    client_socket.connect(socket_path)
    print('已连接得到服务器，输入消息并按回车键发送。输入quit推出。')

    while True:
        message = input(">")
        if message.lower() == 'quit':
            break
        
        client_socket.send(message.encode('utf-8'))


finally:
    client_socket.close()
    print("客户端已关闭")
    