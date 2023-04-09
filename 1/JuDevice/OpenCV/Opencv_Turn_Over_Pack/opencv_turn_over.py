#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/1 22:05
# @Author  : Jun_军
# @File    : opencv_turn_over.py
from copy import deepcopy
from cv2 import flip, warpAffine
from numpy import float32


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

    def opencv_imitation_func(self, img, num1, num2, num3, num4, num5, num6):
        try:
            rows, cols, channel = img.shape
            M = float32([[float(num1), float(num2), float(num3)],
                         [float(num4), float(num5), float(num6)]])
            dst = warpAffine(deepcopy(img), M=M, dsize=(cols, rows))
            result = [True, [dst], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
