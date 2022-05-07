import socket
# import time


def connection():
    '''建立socket连接并配置PGV。
    '''
    ip = '172.28.1.233'
    port = 8899
    socket.setdefaulttimeout(3)  # 设置等待时间
    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 开启套接字
    tcpCliSock.connect((ip, port))  # 建立连接
    print('PGV连接成功')
    while True:
        tcpCliSock.send(b'\xc8\x37')
        data = tcpCliSock.recv(1024)
        print(data)
        print(len(data))


connection()
