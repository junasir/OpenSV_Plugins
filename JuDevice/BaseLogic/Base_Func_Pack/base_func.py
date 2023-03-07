#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/7 22:05
# @Author  : Jun_军
# @File    : base_func.py


class JuBaseFunc(object):
    def __init__(self, log=None):
        self.user_logger = log

    def base_print(self, info, context):
        try:
            if type(info) is str or type(info) is bytes:
                self.user_logger.info(eval(info))
            else:
                self.user_logger.info(str(info))
            result = [True, None, None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
