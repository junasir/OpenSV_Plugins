#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/3/16 21:03
# @Author  : Jun_军
# @File    : seetaface_detection.py
from JuPluginPack.JuDevice.OpenCV.Seetaface_Detection_Pack.seetaface.api import SeetaFace, FACE_DETECT, DetectProperty


class JuSeetafaceDetection(object):
    def __init__(self, log=None):
        self.user_logger = log
        init_mask = FACE_DETECT
        self.seetaFace = SeetaFace(init_mask)

    def opencv_seetaface_detection(self, img, face_piex, confidence):
        try:
            self.seetaFace.SetProperty(DetectProperty.PROPERTY_MIN_FACE_SIZE, int(face_piex))
            self.seetaFace.SetProperty(DetectProperty.PROPERTY_THRESHOLD, float(confidence))
            detect_result = self.seetaFace.Detect(img)
            list_all = []
            for i in range(detect_result.size):
                face = detect_result.data[i].pos
                list_all.append([face.x, face.y, face.width, face.height])
            result = [True, [list_all], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
