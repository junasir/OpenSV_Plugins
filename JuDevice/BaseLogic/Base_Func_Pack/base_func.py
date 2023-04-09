#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/7 22:05
# @Author  : Jun_军
# @File    : base_func.py
import pickle
from json import dumps, loads
import zmq


class JuBaseFunc(object):
    def __init__(self, log=None):
        self.user_logger = log
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5557")

    def base_print(self, info):
        try:
            if type(info) is str or type(info) is bytes:
                self.user_logger.info(eval(info))
            else:
                self.user_logger.info(str(info))
            result = [True, None, None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def socket_info(self, variable):
        try:
            info = {"func": "get_variable_result", "args": ("2",)}
            message = dumps(info, ensure_ascii=False, separators=(',', ':'))
            self.socket.send_string(message)
            response = self.socket.recv()
            rec = response
            try:
                info_new = pickle.loads(rec)
                if "variable_result" in info_new:
                    result_get = info_new["variable_result"]
                    # result_info = pickle.loads(result_get)
                    result = [True, [result_get], None, None]
                else:
                    result = [False, "variable_result not in info", None, None]
            except BaseException as e:
                self.user_logger.error(e)
                result = [False, e, None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def while_info(self, info):
        result = [True, None, None, None]
        return result
