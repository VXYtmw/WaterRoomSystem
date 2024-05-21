import socket
import threading
import time

begin_data = b'Frame Begin'
end_data = b'Frame Over'

maxcache = 1430


def handle_sock(sock, addr):
    print('----------连接建立成功----------')
    temp_data = b''
    # t1 = int(round(time.time() * 1000))

    data = sock.recv(2)
    water_room_id = int.from_bytes(data, byteorder='big')  # 解析开水房ID数据
    print(f"开水房ID: {water_room_id}")

    while True:
        print('-------准备接收下一组数据-------')

        data = sock.recv(1)
        light = bool(int.from_bytes(data, byteorder='big'))
        print(f"光照信息: {light}")

        temp_data = b''  # 用于保存图片数据
        data = sock.recv(maxcache)
        data = data[len(begin_data):len(data)]  # 将第一个数据包的开始标志信息（b'Frame Begin'）清除
        # 判断这一数据包是不是最后一个包。最后一个数据包的结尾是b'Frame Over'
        while data[-len(end_data):] != end_data:
            temp_data = temp_data + data  # 不是结束的包，将数据添加进temp_data
            data = sock.recv(maxcache)  # 继续接受数据，直到接受的数据包包含b'Frame Over'，表示是这张图片的最后一帧
        temp_data = temp_data + data[0:(len(data) - len(end_data))]  # 将最后一个数据包的结束标志信息（b'Frame Over'）去除

        with open('./test.jpg', 'wb') as fp:
            fp.write(temp_data)

        print("接收到的图像信息大小: " + str(len(temp_data)))
        # sock.send("1".encode('utf-8'))
        

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('X.X.X.X', 8080))
server.listen(5)
CONNECTION_LIST = []

# 主线程循环接收客户端连接
while True:
    sock, addr = server.accept()
    CONNECTION_LIST.append(sock)
    print('Connect--{}'.format(addr))
    # 连接成功后开一个线程用于处理客户端
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()
