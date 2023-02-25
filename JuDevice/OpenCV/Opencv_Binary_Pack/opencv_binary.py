from cv2 import cvtColor, COLOR_BGR2GRAY
from cv2 import THRESH_BINARY, THRESH_BINARY_INV, THRESH_TRUNC, THRESH_TOZERO, THRESH_TOZERO_INV,\
    THRESH_OTSU, THRESH_TRIANGLE, threshold


class JuOpencvBinary(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_binary_func(self, img, thresh, maxval, deal_type):
        result = [False, None, None, None]
        try:
            # locals()[deal_type]
            ret, img1 = threshold(src=img, thresh=int(thresh), maxval=int(maxval), type=eval(deal_type))
            # grayImage = cvtColor(img, COLOR_BGR2GRAY)
            # # img = cv2.imread(path)
            result = [True, [ret, img1], None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
