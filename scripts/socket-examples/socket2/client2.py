import socket
import os
#1.定义服务器socket文件路径(需要与服务器一致)
socket_path = "/tmp/my_socket"
#2.创建客户端socket(unix套接字)
client_socket = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)

try:#3.连接服务器（通过socket文件路径)
    client_socket.connect(socket_path)
    print('已连接得到服务器，输入消息并按回车键发送。输入quit推出。')

   # while True:
        #4.接收服务器发送的数据
       # data = client_socket.recv(1024)#1024是缓冲区大小，可根据需求调整
     #   if not data:
        #若服务器关闭连接，data为空，推出循环
           ##   break
    while True:
    # 1. 客户端先发送消息（主动发起）
         message = input("输入消息：")
         client_socket.send(message.encode('utf-8'))
         print("消息已发送")
    # 2. 客户端再接收服务端回复（等待回应）
         data = client_socket.recv(1024)
         if not data:
          print("服务端断开连接")
          break
    
    reply = data.decode('utf-8')
    print(f"收到服务端回复：{reply}")

        #5. 解码数据(与服务器编码一致)
      #  message = data.decode('utf-8')
       # print(f"收到服务器指令：{message}")

        #6.根据指令执行操作
        #if message == "exit":
      #       print("收到退出指令，关闭连接")
       #      break
     #   elif message == "hello":
     #        #示例：回复服务器
          #   client_socket.send("客户端回复：hello".encode('utf-8'))

     #   else:
             #其他指令的处理逻辑
       #     print(f"执行指令：{message}")

finally:
    #7.关闭连接无论是否异常
   client_socket.close()
   print("客户端已关闭")
    