#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/25 13:58
# @Author  : Jun_军
# @File    : opencv_test.py


import cv2


class JuOpencvTest(object):
    def __init__(self, log=None):
        self.user_logger = log
        self.cap = None
        self.cap_id = None
        self.haarcascade = None
        self.path = None

    def opencv_test_func(self, path, mode):
        result = [False, None, None, None]
        try:
            if mode == "video":
                path = int(path)
                if self.cap is None:
                    self.cap = cv2.VideoCapture(path)
                    self.cap_id = path
                if self.cap_id != path:
                    self.cap = cv2.VideoCapture(path)
                ret, image = self.cap.read()
                if ret:
                    img = image
                else:
                    self.user_logger.error("open cap error")
                    return
            else:
                img = cv2.imread(path)
            result = [True, [img], None, None]
        except BaseException as e:
            print(e)
        return result

    def opencv_release(self):
        self.cap.release()

    def opencv_test_show(self, img):
        result = [False, None, None, None]
        try:
            # context_class.img_show(img)
            result = [True, img, True, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result

    def opencv_haarcascade(self, img, scaleFactor, minNeighbors, face_detector):
        try:
            if self.path is None:
                self.haarcascade = cv2.CascadeClassifier(face_detector)
                self.path = face_detector
            if self.path != face_detector:
                self.haarcascade = cv2.CascadeClassifier(face_detector)
            faces = self.haarcascade.detectMultiScale(img, float(scaleFactor), int(minNeighbors))
            result = [True, [faces], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
