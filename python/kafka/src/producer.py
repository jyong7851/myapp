from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from datetime import datetime


def send_kafka():
    producer = KafkaProducer(bootstrap_servers='192.168.1.12:9092')
    msg_dict = {
        "sleep_time": 10,
        "db_config": {
            "database": "test_1",
            "host": "106.12.222.49",
            "user": "root",
            "password": "root"
        },
        "table": "msg",
        "msg": "Hello World"
    }

    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
    parmas_message = json.dumps(msg_dict, ensure_ascii=False)
    try:
        for i in range(1, 10000):
            key = "test001=========" + str(i) + "======="
            v = parmas_message.encode('utf-8')
            k = key.encode('utf-8')

            future = producer.send('test', key=k, value=v)
            record_metadata = future.get(timeout=10)

        producer.close()

    except KafkaError as e:
        print(e)
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
