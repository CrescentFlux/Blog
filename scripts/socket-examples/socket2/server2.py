import socket
server_socket = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
#创建对象，AF_UNIX表示用语本地通信，SOCK_STREAM表示使用TCP协议类似的可靠数据流
socket_path = '/tmp/my_socket'

#绑定地址
import os
if os.path.exists(socket_path):
    os.remove(socket_path)
server_socket.bind(socket_path)

#开始监听连接请求
server_socket.listen(1)
print( '服务器已经启动等待连接 ')

#接受一个客户端的连接
connection,client_address = server_socket.accept()
print("客户端已经连接")

try:
    while True:
        #接收客户端发送的数据
        data =connection.recv(1024)
        
        if not data:
            break
        message = data.decode('utf-8')
        print(f"收到消息:{message}")
    
        ###/////新增功能不仅接受消息，而且回复消息实现本地通讯/////
        reply_message =f"服务器收到：'{message}'"
        connection.send(reply_message.encode('utf-8'))


finally:
    connection.close()
    server_socket.close()
    os.remove(socket_path)#清理socket文件
    print('服务器已关闭')