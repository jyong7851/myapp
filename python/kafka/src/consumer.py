from kafka import KafkaConsumer
import time, zerorpc
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import asyncio, json
from aiohttp import ClientSession

executor = ThreadPoolExecutor(max_workers=50)
weather_list = []
process_on = "waiting"  # 定时器运行标志 ，默认空闲
max_length = 0


# 数据分批提交至dispy
def post_socket_server():
    global max_length
    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:4242")
    c.hello(weather_list)
    c.close()
    weather_list.clear()
    max_length = 0


async def get_web_weather(city):
    async with ClientSession() as session:
        async with session.get("http://wthrcdn.etouch.cn/weather_mini?city=" + city) as response:
            response = await response.read()
            print(response.decode("utf-8"))
            weatherData = json.loads(response.decode("utf-8"))

            weather_dict = dict()
            if weatherData["status"] == 1000:
                weather_dict['city'] = city
                weather_dict['high'] = weatherData['data']['forecast'][0]['high']
                weather_dict['low'] = weatherData['data']['forecast'][0]['low']
                weather_dict['type'] = weatherData['data']['forecast'][0]['type']
                weather_dict['fengxiang'] = weatherData['data']['forecast'][0]['fengxiang']
                weather_dict['ganmao'] = weatherData['data']['ganmao']
            weather_list.append(weather_dict)


def get_city_weather(city):
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_web_weather(city=city))


def kafka_consumer():
    consumer = KafkaConsumer("test", group_id="user-event-test", bootstrap_servers=['192.168.1.12:9092'])
    executor.submit(start_timer)
    for msg in consumer:
        recv = "%s:%d:%d: key=%s value=%s" % (
            msg.topic, msg.partition, msg.offset, msg.key.decode("utf-8"), msg.value.decode("utf-8"))
        #  weather = get_city_weather(city=msg.value.decode("utf-8"))
        # executor.submit(get_city_weather, msg.value.decode("utf-8"))
        get_city_weather(msg.value.decode("utf-8"))
    # weather_list.append(weather)


def start_timer():
    global max_length
    print("======定时器启动========")
    while True:
        print(max_length, len(weather_list))

        if len(weather_list) == max_length and max_length > 0:
            post_socket_server()
        if len(weather_list) > max_length:
            max_length = len(weather_list)

        time.sleep(3)


kafka_consumer()
