#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/25 13:58
# @Author  : Jun_军
# @File    : opencv_gray.py
import cv2
from cv2 import cvtColor, COLOR_BGR2GRAY


class JuOpencvImgSave(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_save_func(self, path, img, context_class):
        result = [False, None, None, None]
        try:
            # grayImage = cvtColor(img, COLOR_BGR2GRAY)
            cv2.imwrite(path, img)
            # img = cv2.imread(path)
            result = [True, None, None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
