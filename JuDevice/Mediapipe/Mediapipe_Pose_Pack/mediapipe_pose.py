from copy import deepcopy
import cv2
import mediapipe as mp


class JuMediapipePose(object):
    def __init__(self, log=None):
        self.user_logger = log

    def mediapipe_pose_det(self, img, min_detection_confidence, min_tracking_confidence):
        try:
            mp_drawing = mp.solutions.drawing_utils

            # 参数：1、颜色，2、线条粗细，3、点的半径
            DrawingSpec_point = mp_drawing.DrawingSpec((0, 255, 0), 5, 1)
            DrawingSpec_line = mp_drawing.DrawingSpec((0, 0, 255), 5, 1)
            new_img = deepcopy(img)
            # mp.solutions.pose，是人的骨架
            mp_pose = mp.solutions.pose
            pose_mode = mp_pose.Pose(min_detection_confidence=min_detection_confidence,
                                     min_tracking_confidence=min_tracking_confidence)
            image1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 处理RGB图像
            results = pose_mode.process(image1)
            mp_drawing.draw_landmarks(
                new_img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, DrawingSpec_point, DrawingSpec_line)

            result = [True, [new_img], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result