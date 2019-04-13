import cv2
import matplotlib.pyplot as plt
import numpy as np

class mser_extraction:

    def __init__(self, IMAGE_PATH):
        self.gray_img = cv2.imread(IMAGE_PATH, 0)
        self.delta = 5
        self.min_area = 60
        self.max_area = 14400
        self.variation = 0.25

    def extraction(self):
        mser = cv2.MSER_create()
        msers, bboxes = mser.detectRegions(grayImg256)
        return msers, bboxes

    def extraction_with_labels(self):
        rect_img = self.gray_img.copy()
        binarized = np.zeros_like(grayImg256)
        msers, bboxes = self.extraction()
        for i,box in enumerate(bboxes):
            if ft800.verification(retImg, msers[i], box):
                rect_img = cv2.rectangle(rect_img, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
                binarized[ msers[i][:, 1], msers[i][:, 0]] = 255
        return rect_img, binarized

    @property
    def delta(self):
        return self.__delta

    @delta.setter
    def delta(self, val):
        self.__delta = val

    @property
    def min_area(self):
        return self.__min_area

    @min_area.setter
    def min_area(self, val):
        self.__min_area = val

    @property
    def max_area(self):
        return self.__max_area

    @max_area.setter
    def max_area(self, val):
        self.__max_area = val

    @property
    def variation(self):
        return self.__variation

    @variation.setter
    def variation(self, val):
        self.__variation = val

