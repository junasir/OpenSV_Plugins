#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/25 13:58
# @Author  : Jun_军
# @File    : opencv_gray.py


from cv2 import cvtColor, COLOR_BGR2GRAY


class JuOpencvGray(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_gray_func(self, img):
        result = [False, None, None, None]
        try:
            grayImage = cvtColor(img, COLOR_BGR2GRAY)
            # img = cv2.imread(path)
            result = [True, [grayImage], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
