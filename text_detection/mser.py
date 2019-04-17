from math import sqrt
import cv2
import matplotlib.pyplot as plt
import numpy as np

class mser_cls:

    def __init__(self, IMAGE_PATH):
        img = cv2.imread(IMAGE_PATH, 0)
        mul = sqrt(img.shape[0]*img.shape[1]/400000)
        self.gray_img = cv2.resize(img, (int(img.shape[1]/mul), int(img.shape[0]/mul)))
        # self.gray_img = cv2.equalizeHist(self.gray_img)
        self.delta = 5
        self.min_area = 9 
        self.max_area =500 
        self.variation = 0.25

    def extraction(self, flt = 0, direction = 0):
        mser = cv2.MSER_create(_delta = self.delta, _min_area = self.min_area, _max_area = self.max_area)
        if direction == 0:
            msers, bboxes = mser.detectRegions(self.gray_img)
        else:
            msers, bboxes = mser.detectRegions(255 - self.gray_img)

        retmsrs = []
        retboxes = []
        if type(flt) != type(0):
            for i in range(len(msers)):
                points = msers[i]
                box = bboxes[i]
                if flt.verification(points,box) == False:
                    continue
                else:
                    retmsrs.append(points)
                    retboxes.append(box)
        else:
            retmsrs = msers
            retboxes = bboxes
        return retmsrs, retboxes

    def extraction_with_labels(self, flt = None, direction = 0):
        rect_img = self.gray_img.copy()
        binarized = np.zeros_like(self.gray_img)
        msers, bboxes = self.extraction(flt, direction)
        for i,box in enumerate(bboxes):
            rect_img = cv2.rectangle(rect_img, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
            binarized[ msers[i][:, 1], msers[i][:, 0]] = 255
        return rect_img, binarized

    def extraction_with_labels_verbose(self, flt = None, direction = 0):
        rect_img = self.gray_img.copy()
        binarized = np.zeros_like(self.gray_img)
        colorized = np.uint8(np.ndarray((self.gray_img.shape[0], self.gray_img.shape[1], 3)))
        colorized[:,:,:] = 0

        msers, bboxes = self.extraction(flt, direction)
        for i,box in enumerate(bboxes):
            rect_img = cv2.rectangle(rect_img, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
            binarized[ msers[i][:, 1], msers[i][:, 0]] = 255
            colorized = self.verbose_colorRegion(colorized, msers[i])
            if i < 2000:
                tmp = colorized.copy()
                tmp[:,:,:] = 0
                tmp = self.verbose_colorRegion(tmp, msers[i])
                tmp = cv2.rectangle(tmp, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
                plt.ion()
                plt.imshow(tmp)
                plt.show()
                plt.pause(0.5)
        return rect_img, binarized, colorized, msers, bboxes

    def verbose_colorRegion(self, img, region):
        img[region[:, 1], region[:, 0], 0] = np.random.randint(low=100, high=256)
        img[region[:, 1], region[:, 0], 1] = np.random.randint(low=100, high=256)
        img[region[:, 1], region[:, 0], 2] = np.random.randint(low=100, high=256)
        return img

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

