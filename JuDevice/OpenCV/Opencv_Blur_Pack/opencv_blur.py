#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/27 23:07
# @Author  : Jun_军
# @File    : opencv_bgr_split.py

from cv2 import blur


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