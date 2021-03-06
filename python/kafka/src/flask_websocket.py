from flask import Flask, render_template
from flask_socketio import SocketIO
import random

async_mode = None
app = Flask(__name__)
socket_io = SocketIO()  # 通信类
socket_io.init_app(app)


# @app.route('/')
def index():
    return render_template('index.html', async_mode=socket_io.async_mode)


@ socket_io.on('request_for_response', namespace='/test_conn')
def test_connect(msg):
    print(msg.get("data"))
    while True:
        socket_io.sleep(5)
        t = random_int_list(1, 100, 10)
        print(t)
        socket_io.emit('response',
                      {'data': t},
                      namespace='/test_conn')


def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


if __name__ == '__main__':
    socket_io.run(app,port =5001)
