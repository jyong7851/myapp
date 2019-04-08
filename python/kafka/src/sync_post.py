from gevent import monkey
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request,make_response, render_template
from concurrent.futures import ThreadPoolExecutor

import time
monkey.patch_all()
executor = ThreadPoolExecutor(max_workers=2)
app = Flask(__name__)
app.config.update( DEBUG=True )
@app.route('/asyn/1/', methods=['GET'])
def test_asyn_one():
    s ="hello"
    if request.method == 'GET':
        time.sleep(15)
        s += " sync "

    return s
s ="222222"
def do_update(t):
    global s
    time.sleep(t)
    s="3333333333333333333"
    rst = make_response(s)
    print('start update')
def do_update1():
    global s
    time.sleep(3)
    s="44444444444444"
    print('start update1')
# @app.after_request
def foot_log(response):
    if request.path != "/test":
        print("有客人访问了",request.path)
        response = make_response(s)

    return response

@app.route('/test/', methods=['GET'])
def test():
    print("hello test")
    print("============")
    global s
    s ="22222222"
    response = make_response(s)

    print("---------------")
   # do_update(3)
    return response,201


@app.route('/test1/', methods=['GET'])
def test1():
    print("===============")
    producer = KafkaProducer(bootstrap_servers='192.168.1.12:9092')
    return render_template('index.html'),201







