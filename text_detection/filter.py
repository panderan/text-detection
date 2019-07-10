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
import math
from text_detection.swt import swt

## 几何过滤类
#
class basicFilter:
    
    ## 构造函数
    #
    # @param gray_img 待过滤的灰度图像（MSER 选区从该图像中提取）
    #
    def __init__(self, gray_img=0):
        self.area_lim = 0
        self.perimeter_lim = 12
        self.aspect_ratio_lim = (1.0, 15.0)
        self.aspect_ratio_gt1 = True
        self.occupation_lim = (0.15, 0.90)
        self.compactness_lim = (3e-3, 1e-1)
        self.width_lim = (0, 800)
        self.height_lim = (0, 800)

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
    def verification(self, region, box, debug=False):
        
        # 长宽度过滤
        debug and print("---------------------\n")
        debug and print("Width:%.3f[%.3f, %.3f]" % \
                        (box[2],self.width_lim[0], self.width_lim[1]))
        if box[2] < self.width_lim[0] or box[2] > self.width_lim[1]:
            return False
        debug and print("Height:%.3f[%.3f, %.3f]" % \
                        (box[3],self.height_lim[0], self.height_lim[1]))
        if box[3] < self.height_lim[0] or box[3] > self.height_lim[1]:
            return False

        # 周长
        retval = self.getPerimeter(box)
        debug and print("Perimeter:%.3f [>%.3f]" \
                        % (retval, self.perimeter_lim))
        if retval <  self.perimeter_lim:
            return False
        # 横纵比
        retval = self.getAspectRatio(region)
        rg_area = self.getArea(region)
        debug and print("AspectRatio:%.3f [%.3f,%.3f](%.3f)" \
                        % (retval, self.aspect_ratio_lim[0], self.aspect_ratio_lim[1], rg_area))
        if retval < self.aspect_ratio_lim[0] or retval > self.aspect_ratio_lim[1]:
            return False
        # 占用率
        retval = self.getOccurpiedRatio(region, box)
        debug and print("OccurpiedRatio:%.3f [%.3f,%.3f]" \
                        % (retval, self.occupation_lim[0], self.occupation_lim[1]))
        if retval < self.occupation_lim[0] or retval > self.occupation_lim[1]:
            return False
        # 紧密度
        retval = self.getCompactness(region, box)
        debug and print("Compactness:%.3f [%.3f,%.3f]" \
                        % (retval, self.compactness_lim[0], self.compactness_lim[1]))
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
        box = np.int0(cv2.boxPoints(cv2.minAreaRect(region)))
        p0=np.array(box[-1])
        p1=np.array(box[0])
        p2=np.array(box[1])
        l1=p1-p0
        l2=p1-p2
        h=l1
        w=l2
        
        if (l1[0] == 0 and l1[1] == 0)\
            or (l2[0] == 0 and l2[1] == 0):
            return 9999

        angle = math.asin(l1[1]/math.hypot(l1[0],l1[1]))
        if angle > -math.pi/4 and angle < math.pi/4:
            w=l1
            h=l2    

        dw=math.hypot(w[0],w[1])+1
        dh=math.hypot(h[0],h[1])+1

        ratio = dw/dh
        if self.aspect_ratio_gt1 and ratio < 1.0:
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


class areaAspectFilter:
    def __init__(self):
        self.area_lim = (0, 500)
        self.aspect_lim = (1.0, 15.0)
        pass

    def verification(self, box, debug=False):
        debug and print("---------------------")

        retval = self._get_box_area(box)
        debug and print("Area:%.3f [%d,%d]"\
                         % (retval[0], self.area_lim[0], self.area_lim[1]))
        if retval[0] < self.area_lim[0] or retval[0] > self.area_lim[1]:
            return False

        debug and print("AspectRatio:%.3f [%.3f,%.3f]" \
                        % (retval[1]/retval[2], self.aspect_lim[0], self.aspect_lim[1]))
        if retval[1]/retval[2] < self.aspect_lim[0] or retval[1]/retval[2] > self.aspect_lim[1]:
            return False
        
        return True

    def _get_box_area(self, box):
        p0=np.array(box[-1])
        p1=np.array(box[0])
        p2=np.array(box[1])
        l1=p1-p0
        l2=p1-p2
        h=l1
        w=l2
        angle = math.asin(l1[1]/math.hypot(l1[0],l1[1]))
        if angle > -math.pi/4 and angle < math.pi/4:
            w=l1
            h=l2    

        dw=math.hypot(w[0],w[1])+1
        dh=math.hypot(h[0],h[1])+1
        return (dw*dh, dw, dh)


class swtFilter:
    def __init__(self, gray_img):
        self._swt = swt(gray_img)
        pass
        
    def verification(self, box, debug=False):
        xywh = (box[:,0].min(), 
                box[:,1].min(), 
                box[:,0].max()-box[:,0].min(), 
                box[:,1].max()-box[:,1].min())

        stroke_widths, stroke_widths_opp = self._swt.get_strokes(xywh)
        stroke_widths = np.append(stroke_widths, stroke_widths_opp, axis=0)
        retval = self._swt.get_stroke_properties(stroke_widths)

        total_cnt = len(stroke_widths)
        sw, sw_cnt, mean, std, maxval, minval = retval
        debug and print("total:%d mode:%.2f mode_cnt:%.2f mean:%.2f std:%.2f maxval:%.2f minval:%.2f" \
                        % (total_cnt, sw, sw_cnt, mean, std, maxval, minval))
        
        if sw < 1.5:
            return False    
        if total_cnt < 30:
            return True
        if std < 0.5 or std > 2.5:
            return False
        if mean < 2.0 or mean > 5.0:
            return False 
        return True








