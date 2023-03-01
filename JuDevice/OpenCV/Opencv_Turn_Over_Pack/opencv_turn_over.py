#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/1 22:05
# @Author  : Jun_军
# @File    : opencv_turn_over.py

from cv2 import flip


class JuOpencvTurnOver(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_turn_over_func(self, img, num):
        try:
            flip_img = flip(img, int(num))
            result = [True, [flip_img], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result