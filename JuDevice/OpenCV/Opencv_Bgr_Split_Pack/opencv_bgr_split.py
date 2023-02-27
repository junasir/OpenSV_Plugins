#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/27 23:07
# @Author  : Jun_军
# @File    : opencv_bgr_split.py

from cv2 import split


class JuOpencvBgrSplit(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_bgr_split_func(self, img):
        try:
            b, g, r = split(img)
            result = [True, [b, g, r], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result