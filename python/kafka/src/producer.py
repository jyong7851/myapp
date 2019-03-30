from kafka import KafkaProducer
import json
from datetime import  datetime
producer = KafkaProducer(bootstrap_servers='106.12.222.49:9092')
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
parmas_message = json.dumps(msg_dict,ensure_ascii=False)
for i in range(1,10000):

    key ="test001=========" + str(i) +"======="
    v = parmas_message.encode('utf-8')
    k = key.encode('utf-8')
    producer.send('test',  key=k,value=v)
producer.close()
dt = datetime.now()
print(dt.strftime("%H:%M:%S %f"))