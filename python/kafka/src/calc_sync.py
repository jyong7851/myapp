import uuid, time, json, zerorpc
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify, request, make_response, render_template
import gevent.pywsgi
import gevent
from gevent import monkey

monkey.patch_all()
app = Flask(__name__)

_USER_QUEUE_DICT = {}


class HelloRPC(object):
    i = 0

    def hello(self, uuid, name):
        self.i = int(name)
        if (uuid in _USER_QUEUE_DICT.keys()):
            _USER_QUEUE_DICT[uuid].put(name)
        return "Hello, %s" % name


class SyncCalc(object):
    socket = {
        "server_name": "",
        "port": "4343"
    }

    def __init__(self, id):
        # self._uid = str(uuid.uuid4())
        self._uid = id

        print("======" + self._uid + "=========")
        _USER_QUEUE_DICT[self._uid] = Queue()
        self.write_to_kafka()

    def write_to_kafka(self, params):
        print("======write to kafka=========")
        print("uuid='" + self._uid + "'")
        print("socket:%s" % str(self.socket))
        print("params:%s" % str(params))

    def get_response(self):
        ret = {}
        queue = _USER_QUEUE_DICT[self._uid]
        try:
            ret['data'] = queue.get(timeout=60)  # 十秒后断开，再连
            ret['status'] = True
            _USER_QUEUE_DICT.pop(self._uid)
        except Empty as e:
            ret['status'] = False
        print(_USER_QUEUE_DICT)
        return ret


class TgSyncCalc(SyncCalc):

    def write_to_kafka(self):
        print("==========write OK=================")
        tg_list = ["1101", "1102", "1103"]
        # super().write_to_kafka(tg_list)


executor = ThreadPoolExecutor(max_workers=5)


def start_server():
    s = zerorpc.Server(HelloRPC())
    s.bind("tcp://0.0.0.0:4242")
    s.run()


@app.route('/test', methods=['GET', 'POST'])
def test():
    id = request.form['id']
    print(id)
    calc = TgSyncCalc(id)

    calc.write_to_kafka()
    executor.submit(start_server)
    ret = str(calc.get_response())
    response = make_response(ret)
    return response, 201


if __name__ == "__main__":
    gevent_server = gevent.pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    gevent_server.serve_forever()
