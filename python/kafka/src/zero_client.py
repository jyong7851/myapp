import zerorpc
from datetime import  datetime
from concurrent.futures import ThreadPoolExecutor
# from kazoo.client import KazooClient

'''

zk = KazooClient(hosts="106.12.222.49:2181")
zk.start()
print(zk.exists("/sg/city/beijing"))
print(zk.get("/sg/city/beijing"))
'''
def post_range(rg):
    '''
      for i in rg:
        i += i
    :param rg:
    :return:
    '''
    for i in rg:
        c = zerorpc.Client()
        c.connect("tcp://127.0.0.1:4242")
        c.hello(i)
        c.close()
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
def pool_post():
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))
    executor = ThreadPoolExecutor(max_workers=5)
    rg =range(1,1000)
    executor.submit(post_range,(rg))
    rg =range(1000,2000)
    executor.submit(post_range,(rg))
    rg =range(2000,3000)
    executor.submit(post_range,(rg))
    rg =range(3000,4000)
    executor.submit(post_range,(rg))

    print("--------------")
def post():
    print("_____________")
    rg = range(1, 4000)
    post_range(rg)
    print("_____________")
    dt = datetime.now()
    print(dt.strftime("%H:%M:%S %f"))

dt = datetime.now()
print(dt.strftime("%H:%M:%S %f"))
pool_post()
# post()

