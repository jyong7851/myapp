from kafka import KafkaConsumer
from datetime import datetime
consumer = KafkaConsumer('test',group_id = "user-event-test", bootstrap_servers=['106.12.222.49:9092'])
for msg in consumer:
    recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
    print(recv)
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))