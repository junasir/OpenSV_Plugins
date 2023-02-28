#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/27 23:07
# @Author  : Jun_军
# @File    : opencv_bgr_split.py

from cv2 import GaussianBlur


class JuOpencvGaussianBlur(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_gaussian_blur_func(self, img, ksize, sigmaX):
        try:
            ksize = int(ksize)
            sigmaX = int(sigmaX)
            img_gaussianBlur = GaussianBlur(img, (ksize, ksize), sigmaX)
            result = [True, [img_gaussianBlur], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result