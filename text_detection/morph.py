import cv2

class morph:
    def __init__(self):
        pass

    def opening(bins):
        ubit = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        reimg = cv2.dilate(cv2.erode(bins, ubit), ubit)
        return reimg

    def closeing(bins):
        ubit = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        reimg = cv2.erode(cv2.dilate(bins, ubit), ubit)
        return reimg
