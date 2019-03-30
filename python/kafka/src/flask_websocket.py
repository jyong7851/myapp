from flask import Flask, render_template
from flask_socketio import SocketIO
import random

async_mode = None
app = Flask(__name__)
socketio = SocketIO()
socketio.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('request_for_response', namespace='/test_conn')
def test_connect(msg):
    print(msg.get("param"))
    while True:
        socketio.sleep(5)
        t = random_int_list(1, 100, 10)
        socketio.emit('response',
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
    socketio.run(app,port=5001, host='0.0.0.0',debug=True)
