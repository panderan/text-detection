#!/usr/bin/env python

'''
    @package text_detection

    @file filter.py
    几何条件过滤类

    @author panderan@163.com
'''

import math
from enum import Enum
import cv2
import numpy as np
from gui.text_detection.swt import swt


class TdFilterCheckType(Enum):
    '''
    需要检查的类型
    '''
    AREA = 1
    WIDTH = 2
    HEIGH = 4
    PERIMETER = 8
    ASPECTRATIO = 16
    OCCURPIEDRATIO = 32
    COMPACTNESS = 64
    SWT = 128


class TdFilter:
    ''' 简单特征过滤
    '''
    def __init__(self, gray_img=None):
        self.flag = None
        self.area_lim = 0
        self.perimeter_lim = 12
        self.aspect_ratio_lim = [1.0, 15.0]
        self.aspect_ratio_gt1 = True
        self.occupation_lim = [0.15, 0.90]
        self.compactness_lim = [3e-3, 1e-1]
        self.width_lim = [0, 800]
        self.height_lim = [0, 800]

        self.swt = None
        self.canny_image = None
        self.gray_image = gray_img
        self.debug_enable = True
        self.debug_data = {}

    def validate(self, region, box):
        ''' 验证单个选区是否满足条件
        Args:
            region: MSER 提取的选区所有像素点列表
            box: MSER 提取的选区外接矩形
        Returns:
            True 满足
            False 不满足
        '''
        # 长宽度过滤
        if self.flag & TdFilterCheckType.AREA.value:
            self.debug_data['width'] = None if not self.debug_enable else box[2]
            if box[2] < self.width_lim[0] or box[2] > self.width_lim[1]:
                return False
            self.debug_data['height'] = None if not self.debug_enable else box[3]
            if box[3] < self.height_lim[0] or box[3] > self.height_lim[1]:
                return False

        # 周长
        if self.flag & TdFilterCheckType.PERIMETER.value:
            retval = self.getPerimeter(box)
            self.debug_data['perimeter'] = None if not self.debug_enable else retval
            if retval < self.perimeter_lim:
                return False

        # 横纵比
        if self.flag & TdFilterCheckType.ASPECTRATIO.value:
            retval = self.getAspectRatio(region)
            self.debug_data['aspect_ratio'] = None if not self.debug_enable else retval
            if retval < self.aspect_ratio_lim[0] or retval > self.aspect_ratio_lim[1]:
                return False

        # 占用率
        if self.flag & TdFilterCheckType.OCCURPIEDRATIO.value:
            retval = self.getOccurpiedRatio(region, box)
            self.debug_data['occurpied_ratio'] = None if not self.debug_enable else retval
            if retval < self.occupation_lim[0] or retval > self.occupation_lim[1]:
                return False

        # 紧密度
        if self.flag & TdFilterCheckType.COMPACTNESS.value:
            retval = self.getCompactness(region, box)
            self.debug_data['compactness'] = None if not self.debug_enable else retval
            if retval < self.compactness_lim[0] or retval > self.compactness_lim[1]:
                return False

        if self.flag & TdFilterCheckType.SWT.value:
            xywh = (box[:, 0].min(),
                    box[:, 1].min(),
                    box[:, 0].max()-box[:, 0].min(),
                    box[:, 1].max()-box[:, 1].min())
            if self.swt is None:
                self.swt = swt()
                self.swt.setImage(self.gray_image)
            stroke_widths, stroke_widths_opp = self.swt.get_strokes(xywh)
            stroke_widths = np.append(stroke_widths, stroke_widths_opp, axis=0)
            retval = self.swt.get_stroke_properties(stroke_widths)

            total_cnt = len(stroke_widths)
            sw, sw_cnt, mean, std, maxval, minval = retval

            if sw < 1.5:
                return False
            if sw_cnt < 0:
                return False
            if total_cnt < 30:
                return True
            if mean < 2.0 or mean > 5.0:
                return False
            if std < 0.5 or std > 2.5:
                return False
            if maxval < 0:
                return False
            if minval < 0:
                return False

        return True

    def getArea(self, region):
        ''' 获取选区面积
        '''
        return len(region)

    def getPerimeter(self, box):
        ''' 获取选区周长
        '''
        tmp = self.canny_image[box[1]:box[1]+box[3], box[0]:box[0]+box[2]]
        return len(np.where(tmp != 0)[0])

    def getAspectRatio(self, region):
        ''' 获取选区横纵比
        '''
        box = np.int32(cv2.boxPoints(cv2.minAreaRect(region)))
        p0 = np.array(box[-1])
        p1 = np.array(box[0])
        p2 = np.array(box[1])
        l1 = p1-p0
        l2 = p1-p2
        h = l1
        w = l2

        if (l1[0] == 0 and l1[1] == 0)\
            or (l2[0] == 0 and l2[1] == 0):
            return 9999

        angle = math.asin(l1[1]/math.hypot(l1[0], l1[1]))
        if angle > -math.pi/4 and angle < math.pi/4:
            w = l1
            h = l2

        dw = math.hypot(w[0], w[1])+1
        dh = math.hypot(h[0], h[1])+1

        ratio = dw/dh
        if self.aspect_ratio_gt1 and ratio < 1.0:
            ratio = 1.0 / ratio

        return ratio

    def getOccurpiedRatio(self, region, box):
        ''' 获取选区占有率
        '''
        return float(self.getArea(region)) / (float(box[2]) * float(box[3]))

    def getCompactness(self, region, box):
        ''' 获取选区紧密度
        '''
        return float(self.getArea(region)) / float(self.getPerimeter(box)**2)

    def __setConfigItem(self, keystr, config):
        ''' 设置单个参数
        '''
        try:
            if keystr == "flag":
                self.flag = config['flag']
            elif keystr == "area_lim":
                self.area_lim = config['area_lim']
            elif keystr == "perimeter_lim":
                self.perimeter_lim = config['perimeter_lim']
            elif keystr == "aspect_ratio_lim":
                self.aspect_ratio_lim = config['aspect_ratio_lim']
            elif keystr == "aspect_ratio_gt1":
                self.aspect_ratio_gt1 = config['aspect_ratio_gt1']
            elif keystr == "occupation_lim":
                self.occupation_lim = config['occupation_lim']
            elif keystr == "compactness_lim":
                self.compactness_lim = config['compactness_lim']
            elif keystr == "width_lim":
                self.width_lim = config['width_lim']
            elif keystr == "height_lim":
                self.height_lim = config['height_lim']
            else:
                pass
        except KeyError:
            pass
        return None

    def setConfig(self, config):
        ''' 设置参数
        '''
        self.__setConfigItem("flag", config)
        self.__setConfigItem("area_lim", config)
        self.__setConfigItem("perimeter_lim", config)
        self.__setConfigItem("aspect_ratio_lim", config)
        self.__setConfigItem("aspect_ratio_gt1", config)
        self.__setConfigItem("occupation_lim", config)
        self.__setConfigItem("compactness_lim", config)
        self.__setConfigItem("width_lim", config)
        self.__setConfigItem("height_lim", config)
        try:
            if not config['enable']:
                return None
        except KeyError:
            pass

        self.printParams()
        return self

    def printParams(self):
        ''' 打印当前参数
        '''
        params = {"flag": self.flag,
                  "area_lim": self.area_lim,
                  "perimeter_lim": self.perimeter_lim,
                  "aspect_ratio_lim": self.aspect_ratio_lim,
                  "aspect_ratio_gt1": self.aspect_ratio_gt1,
                  "occupation_lim": self.occupation_lim,
                  "compactness_lim": self.compactness_lim,
                  "width_lim": self.width_lim,
                  "height_lim": self.height_lim}
        print("Filter Params %s" % params)

    @property
    def gray_img(self):
        ''' 灰度图像
        '''
        return self.__gray_image
    @gray_img.setter
    def gray_img(self, val):
        if val is not None:
            self.__gray_image = val
            v = np.median(self.__gray_image)
            lower = int(max(0, (1.0 - 0.33) * v))
            upper = int(min(255, (1.0 + 0.33) * v))
            self.canny_image = cv2.Canny(self.__gray_image, lower, upper)
        else:
            self.__gray_image = None
            self.canny_image = None
