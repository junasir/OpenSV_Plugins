#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/6 19:26
# @Author  : Jun_军
# @File    : opencv_hough.py
from copy import deepcopy

from cv2 import HoughLines, Canny, line, TM_CCOEFF_NORMED, CV_16S, matchTemplate, rectangle, Laplacian, convertScaleAbs
from numpy import pi, cos, sin


class JuOpencvHough(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_line_func(self, img, num1, num2, num3):
        try:
            lines = HoughLines(img, int(num1), pi/180, int(num3))
            coordinate = []
            for line in lines:
                rho, theta = line[0]
                a = cos(theta)
                b = sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * a)
                coordinate.append([x1, y1, x2, y2])
            result = [True, [coordinate], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_canny_func(self, img, num1, num2, num3):
        try:
            edges = Canny(deepcopy(img), int(num1), int(num2), apertureSize=int(num3))
            result = [True, [edges], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_draw_line_func(self, coordinate, img):
        try:
            image = deepcopy(img)
            for i in range(len(coordinate)):
                line(image, (coordinate[i][0], coordinate[i][1]), (coordinate[i][2], coordinate[i][3]), (0, 0, 255), 2)
            result = [True, [image], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_template_match_func(self, ori_img, template_img, method, confidence):
        try:
            height, width, c = template_img.shape
            results = matchTemplate(ori_img, template_img, eval(method))
            loc = []
            for i in range(len(results)):
                for j in range(len(results[i])):
                    if results[i][j] > float(confidence):
                        loc.append((j, i, j + width, i + height))
            result = [True, [loc], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_draw_rectangle_func(self, coordinate, img):
        try:
            image = deepcopy(img)
            for i in range(len(coordinate)):
                rectangle(image, (coordinate[i][0], coordinate[i][1]), (coordinate[i][2], coordinate[i][3]),
                          (0, 0, 255), 2)
            result = [True, [image], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_laplacian_func(self, img, num1, num2):
        try:
            edges = Laplacian(deepcopy(img), CV_16S, ksize=int(num2))
            dst = convertScaleAbs(edges)
            result = [True, [dst], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
