#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/27 23:07
# @Author  : Jun_军
# @File    : opencv_bgr_split.py

from cv2 import blur, erode, dilate
from numpy import uint8, ones


class JuOpencvBlur(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_blur_func(self, img, ksize):
        try:
            ksize = int(ksize)
            img = blur(img, (ksize, ksize))
            result = [True, [img], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_erode_func(self, img, ksize, num):
        try:
            ksize = int(ksize)
            kernel = ones(shape=[ksize, ksize], dtype=uint8)
            img = erode(img, kernel=kernel, iterations=int(num))
            result = [True, [img], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_dilate_func(self, img, ksize, num):
        try:
            ksize = int(ksize)
            kernel = ones(shape=[ksize, ksize], dtype=uint8)
            img = dilate(img, kernel, iterations=int(num))
            result = [True, [img], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
