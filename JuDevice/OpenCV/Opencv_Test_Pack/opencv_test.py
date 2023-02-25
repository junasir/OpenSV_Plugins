import cv2


class JuOpencvTest(object):
    def __init__(self, log=None):
        self.user_logger = log

    def opencv_test_func(self, path):
        result = [False, None, None, None]
        try:
            img = cv2.imread(path)
            result = [True, [img], None, None]
        except BaseException as e:
            print(e)
        return result

    def opencv_test_show(self, img, context_class):
        result = [False, None, None, None]
        try:
            context_class.img_show(img)
            result = [True, None, None, None]
        except BaseException as e:
            result = [False, e, None, None]
        return result
