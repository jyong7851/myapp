import zerorpc
from kazoo.client import KazooClient


zk = KazooClient(hosts="106.12.222.49:2181")
zk.start()
print(zk.exists("/sg/city/beijing"))
print(zk.get("/sg/city/beijing"))


c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
print (c.hello("1"))
