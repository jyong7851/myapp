import zerorpc,json
from kazoo.client import KazooClient
class HelloRPC(object):
    i = 0
    def hello(self, name):
        self.i = self.i+  int(name)
        print(self.i)
        return "Hello, %s" % name

zk = KazooClient(hosts="192.168.1.12:2181")
zk.start()
value = json.dumps({'host': '192.168.1.10', 'port': '4242'})
zk.ensure_path('/socket_server/zeropc_server')
if not zk.exists('/socket_server/zeropc_server/port'):
   zk.create('/socket_server/zeropc_server/port', value.encode(),ephemeral=True)
print(zk.exists("/socket_server/zeropc_server"))
print(zk.get("/socket_server/zeropc_server/port"))



s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()







