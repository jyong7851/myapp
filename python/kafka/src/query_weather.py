from datetime import datetime


def calc_weather(weathers):
    import re
    max_temp = -100
    min_temp = 100
    hot_city = {}
    cold_city = {}
    for weather in weathers:
        if len(weather) > 0:
            high = re.sub("\D", "", weather["high"])
            low = re.sub("\D", "", weather["low"])
            if int(high) > max_temp:
                hot_city = weather
                max_temp = int(high)
            if int(low) < min_temp:
                cold_city = weather
                min_temp = int(low)
    return (hot_city, cold_city)


def calc(weathers):
    import dispy
    nodes = ['127.0.0.1']
    #  启动计算集群，和服务器通信，通信密钥是'secret' # depends 为依赖函数
    cluster = dispy.JobCluster(calc_weather, nodes=nodes, secret='secret', depends=[], loglevel=50)
    jobs = []

    job = cluster.submit((weathers))
    jobs.append(job)
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
    cluster.wait()
    print(len(weathers))
    for job in jobs:
        hot_city, cold_city = job()
        print(hot_city)
        print(cold_city)
    return (hot_city, cold_city)


'''
citys = get_city_name()
calc_weather(citys)
'''
