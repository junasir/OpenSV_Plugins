#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/27 23:07
# @Author  : Jun_军
# @File    : opencv_bgr_split.py
from copy import deepcopy

from cv2 import blur, erode, dilate, inRange, bitwise_and, cvtColor, COLOR_BGR2HSV, RETR_TREE, findContours,\
    CHAIN_APPROX_SIMPLE, rectangle, boundingRect, boxFilter
from numpy import uint8, ones, array


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

    def opencv_hsv_func(self, img, h_min, h_max, s_min, s_max, v_min, v_max):
        try:
            h_min = int(h_min)
            h_max = int(h_max)
            s_min = int(s_min)
            s_max = int(s_max)
            v_min = int(v_min)
            v_max = int(v_max)
            imgHSV = cvtColor(img, COLOR_BGR2HSV)
            lower = array([h_min, s_min, v_min])
            upper = array([h_max, s_max, v_max])
            mask = inRange(imgHSV, lower, upper)
            imgResult = bitwise_and(img, img, mask=mask)
            result = [True, [imgResult], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_contours_func(self, img, img1):
        try:
            img1 = deepcopy(img1)
            img = deepcopy(img)
            contours, hierarchy = findContours(deepcopy(img), RETR_TREE, CHAIN_APPROX_SIMPLE)
            for c in contours:
                x, y, w, h = boundingRect(c)
                print(x, y, w, h)
                if x != 0 and y != 0 and w != img1.shape[1] and h != img1.shape[0]:
                    rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            result = [True, [img1], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_box_filter_func(self, img, ddepth, ksize, normalize):
        try:
            ksize = int(ksize)
            ddepth = int(ddepth)
            normalize = int(normalize)
            img = boxFilter(img, ddepth, (ksize, ksize), normalize=normalize)
            result = [True, [img], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
