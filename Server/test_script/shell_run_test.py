import subprocess

YOLOV5_MASTER_PATH = "/home/ubuntu/yolov5_train/yolov5-master"
WEIGHTS_PATH = "/home/ubuntu/yolov5_train/yolov5-master/graduation_design.pt"
DETECT_PATH = "/home/ubuntu/yolov5_train/yolov5-master/data/images"
# 保存路径： SAVE_PROJECT_PATH + SAVE_NAME 
SAVE_PROJECT_PATH = "/home/ubuntu/yolov5_train/yolov5-master/data/images"
SAVE_NAME = "output_test"

# 要执行的 shell 命令
rm_command = f"rm -r {SAVE_PROJECT_PATH}/{SAVE_NAME}"
detect_command = f"python3 {YOLOV5_MASTER_PATH}/detect.py --source {DETECT_PATH} --weights {WEIGHTS_PATH} --project {SAVE_PROJECT_PATH} --name {SAVE_NAME}"

# 执行 shell 命令，并捕获输出
subprocess.run(rm_command, shell=True)
process = subprocess.Popen(detect_command, stdout=subprocess.PIPE, shell=True)

# 读取命令输出
output, _ = process.communicate()

# 将输出转换为字符串
output_str = output.decode("utf-8")

# 获取排队人数信息
queuing_number = (int)(output_str.split(' ')[1])
print(queuing_number)
