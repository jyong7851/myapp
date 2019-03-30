import zerorpc

class HelloRPC(object):
    i = 0
    def hello(self, name):
        self.i = self.i+  int(name)
        print(self.i)
        return "Hello, %s" % name

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()







