#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/25 13:58
# @Author  : Jun_军
# @File    : opencv_binary.py


from cv2 import THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC, THRESH_TOZERO, THRESH_TOZERO_INV,\
    THRESH_OTSU, THRESH_TRIANGLE, threshold


class JuOpencvBinary(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_binary_func(self, img, thresh, maxval, deal_type):
        try:
            ret, img1 = threshold(src=img, thresh=int(thresh), maxval=int(maxval), type=eval(deal_type))
            result = [True, [ret, img1], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
