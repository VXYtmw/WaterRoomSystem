import socket
import threading
import time
import os
import subprocess

import pymysql


# TCP连接配置
# ---------------------------------------- #
IP_SERVER = 'X.X.X.X'
PORT_TCP = 8080
begin_data = b'Frame Begin'
end_data = b'Frame Over'

maxcache = 1430
# ---------------------------------------- #



# YOLOv5预测配置
# ---------------------------------------- #
YOLOV5_MASTER_PATH = "/home/ubuntu/yolov5_train/yolov5-master"
WEIGHTS_PATH = "/home/ubuntu/yolov5_train/yolov5-master/water_room_system.pt"
DETECT_PATH = "/home/ubuntu/tmp/origin"  # 待检测图片路径。实际路径： DETECT_PATH + {water_room_id}
SAVE_PATH = "/home/ubuntu/tmp/result"  # 检测结果路径。实际路径： SAVE_PATH + {water_room_id}
# ---------------------------------------- #



# 数据库连接配置
# ---------------------------------------- #
DB_HOST = 'localhost'
DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''
DB_TABLE_NAME = ''
# ---------------------------------------- #



def detect(water_room_id):
    # 要执行的 shell 命令
    rm_command = f"rm -r {SAVE_PATH}/{water_room_id}"
    detect_command = f"python3 {YOLOV5_MASTER_PATH}/detect.py " + \
        f" --source {DETECT_PATH}/{water_room_id} --weights {WEIGHTS_PATH} --project {SAVE_PATH} --name {water_room_id}"

    # 执行 shell 命令，并捕获输出
    subprocess.run(rm_command, shell=True)
    process = subprocess.Popen(detect_command, stdout=subprocess.PIPE, shell=True)

    # 读取命令输出
    output, _ = process.communicate()

    # 将输出转换为字符串
    output_str = output.decode("utf-8")

    # 获取排队人数信息
    queuing_number = (int)(output_str.split(' ')[1])
    return queuing_number



def mysql_update(water_room_id, status, queuing_number):
    # 连接到 MySQL 数据库
    connection = pymysql.connect(host=DB_HOST,
                                user=DB_USER,
                                password=DB_PASSWORD,
                                database=DB_NAME,
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # 执行 SQL 查询
            sql = f"UPDATE {DB_TABLE_NAME} SET status = %s, queuing_number = %s WHERE water_room_id = %s"
            cursor.execute(sql, (status, queuing_number, water_room_id))
            
        # 提交事务
        connection.commit()

    finally:
        # 关闭数据库连接
        connection.close()



def handle_sock(sock, addr):
    print('----------连接建立成功----------')
    temp_data = b''
    # t1 = int(round(time.time() * 1000))

    data = sock.recv(2)
    water_room_id = int.from_bytes(data, byteorder='big')  # 解析开水房ID数据
    print(f"开水房ID: {water_room_id}")

    # 新建文件夹用于保存临时数据
    img_detect_path = f'{DETECT_PATH}/{water_room_id}'
    if not os.path.exists(img_detect_path):
        os.makedirs(img_detect_path)
    
    img_save_path = f'{SAVE_PATH}/{water_room_id}'
    if not os.path.exists(img_save_path):
        os.makedirs(img_save_path)

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

        with open(f'{img_detect_path}/{water_room_id}.jpg', 'wb') as fp:
            fp.write(temp_data)
        
        print("接收到的图像信息大小: " + str(len(temp_data)))
        
        # 进行图像检测
        queuing_number = detect(water_room_id)
        print("检测得到的排队人数: ", queuing_number)

        # 更新MySQL数据库
        mysql_update(water_room_id, light, queuing_number)

        # sock.send("1".encode('utf-8'))
        

def run():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_SERVER, PORT_TCP))
    server.listen(5)
    CONNECTION_LIST = []
    print("-------服务器初始化完成-------")

    # 主线程循环接收客户端连接
    while True:
        sock, addr = server.accept()
        CONNECTION_LIST.append(sock)
        print('Connect--{}'.format(addr))
        # 连接成功后开一个线程用于处理客户端
        client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
        client_thread.start()

if __name__ == "__main__":
    run()
