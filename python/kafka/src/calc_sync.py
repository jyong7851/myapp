import uuid,time
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor


class SyncCalc(object):
    _USER_QUEUE_DICT = {}
    _uid = uuid.uuid4()

    def __init__(self,f):
        self.f = f
        pass

    def __call__(self, *args, **kwargs):
        self.f()
        # 长轮询
        self._USER_QUEUE_DICT[self._uid] = Queue()
        return self.get_response()

    @property
    def get_queu(self):
        return self._USER_QUEUE_DICT[self._uid]

    def get_response(self):
        ret = {}
        queue = self._USER_QUEUE_DICT[self._uid]
        try:
            ret['data'] = queue.get(timeout=10)  # 十秒后断开，再连
            ret['status'] = True
        except Empty as e:
            ret['status'] = False
        return ret


@SyncCalc
def write_data_to_kafka():
     '''
     调用http，写kafka队列
     :return:
     '''
     pass


ret = write_data_to_kafka()

print(ret)

