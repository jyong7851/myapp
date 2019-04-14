import uuid, time, json, zerorpc

from flask import Flask, jsonify, request, make_response, render_template
from python.kafka.src.query_weather import calc, calc_weather


class HelloRPC(object):
    aysn_list = []

    def hello(self, list):
        for l in list:
            if l not in self.aysn_list:
                self.aysn_list.append(l)
        print(len(self.aysn_list))
        calc(weathers=self.aysn_list)


def start_server():
    s = zerorpc.Server(HelloRPC())
    s.bind("tcp://0.0.0.0:4242")
    s.run()


start_server()
