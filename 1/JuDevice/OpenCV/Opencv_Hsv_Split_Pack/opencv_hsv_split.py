#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/27 23:07
# @Author  : Jun_军
# @File    : opencv_bgr_split.py

from cv2 import split, cvtColor, COLOR_BGR2HSV


class JuOpencvHsvSplit(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_hsv_split_func(self, img):
        try:
            dst = cvtColor(img, COLOR_BGR2HSV)
            h, s, v = split(dst)
            result = [True, [h, s, v], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result