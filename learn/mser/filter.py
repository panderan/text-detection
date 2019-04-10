import matplotlib.pyplot as plt
import numpy as np
import cv2

class mser_filter:
    
    def __init__(self, grayImg):
        self.area_lim = 0.0
        self.perimeter_lim = 0.0
        self.aspect_ratio_lim = 0.0
        self.occupation_lim = (0.0, 0.0)
        self.compactness_lim = (0.0, 0.0)

        v = np.median(grayImg)
        lower = int(max(0, (1.0 - 0.33) * v))
        upper = int(min(255, (1.0 + 0.33) * v))
        self.edgesImg = cv2.Canny(grayImg, lower, upper)

    def verification(self, img, region, box):
        ## 面积
        retval = self.getArea(region)
        if retval < img.shape[0]*img.shape[1]*self.area_lim:
            return False
        ## 周长
        retval = self.getPerimeter(box)
        if retval <  2 * (img.shape[0] + img.shape[1]) * self.perimeter_lim:
            return False
        ## 横纵比
        retval = self.getAspectRatio(region)
        if retval > self.aspect_ratio_lim:
            return False
        ## 占用率
        retval = self.getOccurpiedRatio(region, box)
        if retval < self.occupation_lim[0] or retval > self.occupation_lim[1]:
            return False
        ## 紧密度
        retval = self.getCompactness(region, box)
        if retval < self.compactness_lim[0] or retval > self.compactness_lim[1]:
            return False
        return True


    def getArea(self, region):
        return len(region)

    def getPerimeter(self, box):
        tmp = self.edgesImg[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
        return len(np.where(tmp != 0)[0])
    
    def getAspectRatio(self, region):
        h = max(region[:, 1]) - min(region[:, 1])
        w = max(region[:, 0]) - min(region[:, 0])
        return float(w) / float(h)
    
    def getOccurpiedRatio(self, region, box):
        return float(self.getArea(region)) / (float(box[2]) * float(box[3]))

    def getCompactness(self, region, box):
        return float(self.getArea(region)) / float(self.getPerimeter(box)**2)

    def debug1(self, img, regions, bboxes, idx):
        region = regions[idx]
        box = bboxes[idx]
        tmp = img.copy()
        tmp = cv2.rectangle(tmp, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), 255)
        tmp[region[:, 1], region[:, 0]] = 255
        plt.imshow(tmp, "gray")

    @property
    def area_lim(self):
        return self.__AREA_LIM

    @area_lim.setter
    def area_lim(self, val):
        self.__AREA_LIM = val
    
    @property
    def perimeter_lim(self):
        return self.__PERIMETER_LIM 

    @perimeter_lim.setter
    def perimeter_lim(self, val):
        self.__PERIMETER_LIM = val

    @property
    def aspect_ratio_lim(self):
        return self.__ASPECT_RATIO_LIM

    @aspect_ratio_lim.setter
    def aspect_ratio_lim(self, val):
        self.__ASPECT_RATIO_LIM = val

    @property
    def occupation_lim(self):
        return self.__OCCUPATION_LIM

    @occupation_lim.setter
    def occupation_lim(self, val):
        self.__OCCUPATION_LIM = val

    @property
    def compactness_lim(self):
        return self.__COMPACTNESS_LIM

    @compactness_lim.setter
    def compactness_lim(self, val):
        self.__COMPACTNESS_LIM = val


class mser_filter800(mser_filter):

    def __init__(self, grayImg):
        super(mser_filter800, self).__init__(grayImg)
        self.area_lim = 2.0e-4
        self.perimeter_lim = 1e-4
        self.aspect_ratio_lim = 5.0
        self.occupation_lim = (0.23, 0.90)
        self.compactness_lim = (3e-3, 1e-1)


