from gevent import monkey
from gevent.pywsgi import WSGIServer
from flask import Flask, jsonify, request

import os,sys
import time
import random

app = Flask(__name__)


@app.route('/asyn/1/', methods=['GET'])
def test_asyn_one():
    s ="hello"
    if request.method == 'GET':
        time.sleep(15)
        s += " sync "
    return s
@app.route('/test/', methods=['GET'])
def test():
    return 'hello test'




if __name__ == "__main__":
    app.run()