#!/usr/bin/env python

## @package text_detection
#   
# @file filter.py
# 几何条件过滤类
#   
# @author panderan@163.com 
#

import matplotlib.pyplot as plt
import numpy as np
import cv2

## 几何过滤类
#
class mser_filter:
    
    ## 构造函数
    #
    # @param gray_img 待过滤的灰度图像（MSER 选区从该图像中提取）
    #
    def __init__(self, gray_img=0):
        self.area_lim = 0.0
        self.perimeter_lim = 0.0
        self.aspect_ratio_lim = 0.0
        self.occupation_lim = (0.0, 0.0)
        self.compactness_lim = (0.0, 0.0)
        self.gray_img = None

        if type(gray_img) != type(0):
            self.gray_img = gray_img
            v = np.median(gray_img)
            lower = int(max(0, (1.0 - 0.33) * v))
            upper = int(min(255, (1.0 + 0.33) * v))
            self.edges_img = cv2.Canny(gray_img, lower, upper)

    ## 验证单个选区是否满足条件
    #
    # @param region MSER 提取的选区所有像素点列表
    # @param box MSER 提取的选区外接矩形
    #
    # @retval True 满足
    # @retval False 不满足
    #
    def verification(self, region, box):
        # tmp = self.gray_img.copy()
        # tmp = cv2.drawContours(tmp, [region], 0, 255, thickness=cv2.FILLED)
        # cv2.namedWindow("Debug",0);
        # cv2.resizeWindow("Debug", 800, 600);
        # cv2.imshow("Debug", tmp)
        # cv2.waitKey(1)

        # 周长
        retval = self.getPerimeter(box)
        if retval <  self.perimeter_lim:
            return False
        # 横纵比
        retval = self.getAspectRatio(region)
        if retval > self.aspect_ratio_lim:
            return False
        # 占用率
        retval = self.getOccurpiedRatio(region, box)
        if retval < self.occupation_lim[0] or retval > self.occupation_lim[1]:
            return False
        # 紧密度
        retval = self.getCompactness(region, box)
        if retval < self.compactness_lim[0] or retval > self.compactness_lim[1]:
            return False
        return True

    ## 获取选区面积
    #
    def getArea(self, region):
        return len(region)
    
    ## 获取选区周长
    #
    def getPerimeter(self, box):
        tmp = self.edges_img[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
        return len(np.where(tmp != 0)[0])

    ## 获取选区横纵比 
    #
    def getAspectRatio(self, region):
        h = max(region[:, 1]) - min(region[:, 1])
        w = max(region[:, 0]) - min(region[:, 0])
        ratio = float(w) /float(h)
        if ratio < 1.0:
            ratio = 1.0 / ratio
        return ratio

    ## 获取选区占有率
    #
    def getOccurpiedRatio(self, region, box):
        return float(self.getArea(region)) / (float(box[2]) * float(box[3]))

    ## 获取选区紧密度
    #
    def getCompactness(self, region, box):
        return float(self.getArea(region)) / float(self.getPerimeter(box)**2)

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

    @property
    def gray_img(self):
        return self.__GRAY_IMG
    @gray_img.setter
    def gray_img(self, val):
        if type(val) == type(np.zeros((3,3))): 
            self.__GRAY_IMG = val 
            v = np.median(self.__GRAY_IMG)
            lower = int(max(0, (1.0 - 0.33) * v))
            upper = int(min(255, (1.0 + 0.33) * v))
            self.__EDGES_IMG = cv2.Canny(self.__GRAY_IMG, lower, upper)
        else:
            self.__GRAY_IMG = None
            self.__EDGES_IMG = None

    @property
    def edges_img(self):
        return self.__EDGES_IMG
    @edges_img.setter
    def edges_img(self, val):
        pass

    def debug1(self, img, regions, bboxes, idx):
        region = regions[idx]
        box = bboxes[idx]
        tmp = img.copy()
        tmp = cv2.rectangle(tmp, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), 255)
        tmp[region[:, 1], region[:, 0]] = 255
        plt.imshow(tmp, "gray")


## 几何过滤类400k
# 其中的默认参数适合图像像素总量为400,000 的图像
#
class mser_filter400k(mser_filter):

    def __init__(self, gray_img=0):
        super(mser_filter400k, self).__init__(gray_img)
        self.area_lim = 0
        self.perimeter_lim = 12
        self.aspect_ratio_lim = 15.0
        self.occupation_lim = (0.15, 0.90)
        self.compactness_lim = (3e-3, 1e-1)
        self.gray_img = None
















