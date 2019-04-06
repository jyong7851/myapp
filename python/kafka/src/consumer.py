from kafka import KafkaConsumer
import time, threading
from concurrent.futures import ThreadPoolExecutor

_batch_nums = 1000  # 1000条数据提交一次
executor = ThreadPoolExecutor(max_workers=5)
kafka_list = []
process_on = "waiting"  # 定时器运行标志 ，默认空闲


# 数据分批提交至socket_server
def post_socket_server():
    global process_on
    gs = 0          # 批提交计数器
    process_on = "running"  # 运行中
    task_list = []

    if len(kafka_list) > 0:
        print("=======list记录数：" + str(len(kafka_list)) + "==============")

    for ka in kafka_list:
        task_list.append(ka)
        kafka_list.remove(ka)
        if gs > _batch_nums:  # 1000一提交
            calc_server(task_list=task_list)
            task_list.clear()
            break
        gs += 1

    if len(task_list) > 0:
        calc_server(task_list=task_list)
        task_list.clear()
    process_on = "waiting"


# 流失计算业务逻辑处理
def calc_server(task_list):
    for t in task_list:
        print(t)


def kafka_consumer():
    consumer = KafkaConsumer('test', group_id="user-event-test", bootstrap_servers=['192.168.1.12:9092'])
    executor.submit(start_timer)
    for msg in consumer:
        recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        kafka_list.append(recv)


def start_timer():
    global timer, process_on
    print("======定时器启动========")
    while True:
        timer = threading.Timer(3, post_socket_server)  # 3秒调用一次函数
        if process_on == "waiting":
            timer.start()  # 启用定时器
        time.sleep(1)


kafka_consumer()
