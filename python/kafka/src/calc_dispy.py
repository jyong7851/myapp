import random
from datetime import datetime


def get_tg_line_loss(tg_id):
    import random
    lv = random.randrange(1, 10000) / 100
    return lv


def calc_tg(tgs):
    good_tgs =[]
    high_tgs =[]
    very_high_tgs = []

    total_good = 0
    total_high = 0
    total_veryhigh = 0
    for tg_id in tgs:
        lv = get_tg_line_loss(tg_id)
        if 0 < lv <= 7:
            total_good += 1
            good_tgs.append({"tg_id":tg_id,"lv":lv})
        if  7 < lv <= 30:
            total_high += 1
            high_tgs.append({"tg_id":tg_id,"lv":lv})
        if lv >30 :
            total_veryhigh += 1
            very_high_tgs.append({"tg_id":tg_id,"lv":lv})
    return (total_good, total_high, total_veryhigh,good_tgs,high_tgs,very_high_tgs)


def load_data():
    tg_list = []
    for i in range(100000):
        tg_list.append(random.randint(1, 10000))
    return tg_list


def calc():
    import dispy
    nodes = ['127.0.0.1']
    #  启动计算集群，和服务器通信，通信密钥是'secret' # depends 为依赖函数
    cluster = dispy.JobCluster(calc_tg, nodes=nodes, secret='secret', depends=[get_tg_line_loss],loglevel=50)
    jobs = []
    datas = load_data()
    job = cluster.submit((datas))
    jobs.append(job)
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
    cluster.wait()
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
    s = ""
    for job in jobs:
        tg_good, tg_high, tg_veryhigh,tgs_good,tgs_high,tgs_veryhigh = job()
        n = 1
        for tg in tgs_good:
            print("第%s个：tg_id:%s,线损率:%s" %(str(n),tg["tg_id"],tg["lv"]))
            n += 1
        s = '本次计算后，合格台区%s个，高损台区%s个，超大损台区%s个' % (tg_good, tg_high, tg_veryhigh)
        print(s)
    return s

