from copy import deepcopy
import cv2
import mediapipe as mp


class JuMediapipeGesture(object):
    def __init__(self, log=None):
        self.user_logger = log
        pass

    def mediapipe_gesture_det(self, img, max_num_hands):
        try:
            mp_drawing = mp.solutions.drawing_utils

            # 参数：1、颜色，2、线条粗细，3、点的半径
            DrawingSpec_point = mp_drawing.DrawingSpec((0, 255, 0), 5, 1)
            DrawingSpec_line = mp_drawing.DrawingSpec((0, 0, 255), 5, 1)
            new_img = deepcopy(img)
            mp_hands = mp.solutions.hands
            hands_mode = mp_hands.Hands(max_num_hands=max_num_hands)
            image1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 处理RGB图像
            results = hands_mode.process(image1)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        new_img, hand_landmarks, mp_hands.HAND_CONNECTIONS, DrawingSpec_point, DrawingSpec_line)

            result = [True, [new_img], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result