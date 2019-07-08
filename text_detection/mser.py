#!/usr/bin/env python

## @package text_detection
#   
# @file mser.py
# 提取一幅图像的 MSER 选区
#   
# @author panderan@163.com 
#

from math import sqrt
import cv2
import matplotlib.pyplot as plt
import numpy as np
from text_detection import common

EXTRACT_NONE=0x0
EXTRACT_RED=0x1
EXTRACT_GREEN=0x2
EXTRACT_BLUE=0x4
EXTRACT_GRAY=0x8
EXTRACT_ALL = EXTRACT_RED + EXTRACT_GREEN + EXTRACT_BLUE + EXTRACT_GRAY
## MSER 连通域提取类
#
# 从一幅灰度图像中提取 MSER 连通域
#
class mser_cls:
    
    ## 构造函数
    # 以灰度图像的形式读入图像，并保持其长宽比将其总像素数量缩放到400,000 左右
    # 
    # @param IMAGE_PATH 输入图像的路径
    def __init__(self):
        self.delta = 5
        self.min_area = 9 
        self.max_area =500 
        self.variation = 0.25
        self.total_pixels = 400000
        self.gamma = 3.0
        self.color_img = None

    ## 提取 MSER 连通区域
    #
    # @param flt 几何条件过滤实例，为 0 则不过滤
    # @param direction MSER 提取方向，0 为 MSER+ ，1 为 MSER-
    # @param channel 在指定通道上提取 MSERs
    #
    # @retval retmsrs 候选连通域列表，每一个元素为包含了该连通域的所有点的列表
    # @retval retboxes 候选连通域列表，每一个元素包含了该连通域的外接矩形
    #
    def extraction(self, flt = 0, direction = 0, channel=EXTRACT_GRAY, debug=False):
        img = None
        if channel == EXTRACT_BLUE:
            img = self.b_img
        elif channel == EXTRACT_GREEN:
            img = self.g_img
        elif channel == EXTRACT_RED:
            img = self.r_img
        elif channel == EXTRACT_GRAY:
            img = self.gray_img
        else:
            return None,None

        mser = cv2.MSER_create(_delta = self.delta, _min_area = self.min_area, _max_area = self.max_area)
        if direction == 0:
            msers, bboxes = mser.detectRegions(img)
        else:
            msers, bboxes = mser.detectRegions(255 - img)

        retmsrs = []
        retboxes = []
        debug_img = debug and np.zeros_like(img)

        if type(flt) != type(0):
            flt.gray_img = img
            for i in range(len(msers)):
                points = msers[i]
                box = bboxes[i]

                ret = flt.verification(points,box,debug)
                if debug:
                    print("%s" % ret)
                    debug_img_temp = debug_img.copy()
                    debug_img_temp = cv2.drawContours(debug_img_temp, [points], 0, 255, thickness=cv2.FILLED)
                    debug_img_show = np.zeros_like(img)
                    debug_img_show[debug_img_temp > 128] = img[debug_img_temp > 128]
                    debug_img_show = cv2.rectangle(debug_img_show, (box[0],box[1]), (box[0]+box[2],box[1]+box[3]),  255, 1)
                    cv2.namedWindow("debug", 0)
                    cv2.resizeWindow("debug", 800, 600)
                    cv2.imshow("debug", debug_img_show)
                    cv2.waitKey(0)

                if ret:
                    retmsrs.append(points)
                    retboxes.append(box)
                else:
                    continue

                if debug:
                    debug_img = cv2.drawContours(debug_img, [points], 0, 255, thickness=cv2.FILLED)
        else:
            retmsrs = msers
            retboxes = bboxes
        return retmsrs, retboxes

    ## 提取 MSER 连通区域（带标记）
    #
    # @param flt 几何条件过滤实例，为 0 则不过滤
    # @param direction MSER 提取方向，0 为 MSER+ ，1 为 MSER-
    # @param channel 在指定通道上提取 MSERs
    #
    # @retval rect_img 在原图中用矩形标出候选区域图像
    # @retval binarized 以背景图像为0，提取的连通域为255 的二值图像
    #
    def extraction_with_labels(self, color_img=None, flt = 0, direction = 0, channel=EXTRACT_GRAY, debug=False):
        if color_img != None:
            self.color_img = color_img
        rect_img = self.gray_img.copy()
        binarized = np.zeros_like(self.gray_img)
        msers, bboxes = self.extraction(flt, direction, channel, debug=debug)
        for i,box in enumerate(bboxes):
            rect_img = cv2.rectangle(rect_img, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
            binarized[ msers[i][:, 1], msers[i][:, 0]] = 255
        return rect_img, binarized


    ## 提取所有通道的 MSER，包括R，G，B，Gray
    #
    # @param flt 几何条件过滤实例，为 0 则不过滤
    # @param direction MSER 提取方向，0 为 MSER+ ，1 为 MSER-
    # @param channel 在指定通道上提取 MSERs
    #
    # @retval binarized 以背景图像为0，提取的连通域为255 的二值图像
    #
    def extraction_in_channels_with_labels(self, color_img, channel, flt = 0, direction = 0, debug=False):
        self.color_img = color_img
        ret_binaries = np.zeros_like(self.gray_img)

        if (channel & EXTRACT_GRAY):
            grect, gbinaries = self.extraction_with_labels(flt = flt, channel=EXTRACT_GRAY, debug=debug)
            ret_binaries[gbinaries > 128] = gbinaries[gbinaries > 128]
        if (channel & EXTRACT_BLUE):
            b_rect, b_binaries = self.extraction_with_labels(flt = flt, channel=EXTRACT_BLUE, debug=debug)
            ret_binaries[b_binaries > 128] = b_binaries[b_binaries > 128]
        if (channel & EXTRACT_GREEN):
            g_rect, g_binaries = self.extraction_with_labels(flt = flt, channel=EXTRACT_GREEN, debug=debug)
            ret_binaries[g_binaries > 128] = g_binaries[g_binaries > 128]
        if (channel & EXTRACT_RED):
            r_rect, r_binaries = self.extraction_with_labels(flt = flt, channel=EXTRACT_RED, debug=debug)
            ret_binaries[r_binaries > 128] = r_binaries[r_binaries > 128]

        return ret_binaries 

    def _preprocessing(self, gimg):
        kel5 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        tophat = cv2.morphologyEx(gimg, cv2.MORPH_TOPHAT, kel5)
        cy = cv2.Canny(tophat, 0, 100)
        sobely = cv2.Sobel(cy, -1, 1, 0)
        blur = cv2.GaussianBlur(sobely, (51,51), 0)
        blurf = blur/blur.max()
        a = np.uint8(gimg * blurf)
        equ = cv2.equalizeHist(a)
        tp = equ/255.0
        o = np.power(tp, self.gamma)
        a = np.uint8(o*255.0)
        return a

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

    @property
    def total_pixels(self):
        return self.__total_pixels
    @total_pixels.setter
    def total_pixels(self, val):
        self.__total_pixels = val
    
    @property
    def color_img(self):
        return self.__color_img
    @color_img.setter
    def color_img(self, val):
        if type(val) == type(np.zeros((3,3))):
            color_img = val
            gimg = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
            mul = sqrt(gimg.shape[0]*gimg.shape[1]/self.total_pixels)
            self.__color_img = cv2.resize(color_img, (int(gimg.shape[1]/mul), int(gimg.shape[0]/mul)))
            b_img = cv2.resize(color_img[:,:,0], (int(gimg.shape[1]/mul), int(gimg.shape[0]/mul)))
            self.__b_img = self._preprocessing(b_img)
            g_img = cv2.resize(color_img[:,:,1], (int(gimg.shape[1]/mul), int(gimg.shape[0]/mul)))
            self.__g_img = self._preprocessing(g_img)
            r_img = cv2.resize(color_img[:,:,2], (int(gimg.shape[1]/mul), int(gimg.shape[0]/mul)))
            self.__r_img = self._preprocessing(r_img)
            gimg = cv2.resize(gimg, (int(gimg.shape[1]/mul), int(gimg.shape[0]/mul)))
            self.__orig_gray_img = gimg
            self.__gray_img = self._preprocessing(gimg)
        else:
            self.__gray_img = None
            self.__b_img = None
            self.__g_img = None
            self.__r_img = None
    
    @property
    def gray_img(self):
        return self.__orig_gray_img
    @gray_img.setter
    def gray_img(self, val):
        pass

    @property
    def prep_gray_img(self):
            return self.__gray_img
    @prep_gray_img.setter
    def prep_gray_img(self, val):
        pass

    @property
    def b_img(self):
        return self.__b_img
    @b_img.setter
    def b_img(self, val):
        pass

    @property
    def g_img(self):
        return self.__g_img
    @g_img.setter
    def g_img(self, val):
        pass

    @property
    def r_img(self):
        return self.__r_img
    @r_img.setter
    def r_img(self, val):
        pass

    ## 选区着色
    def debug_colorRegion(self, img, region):
        img[region[:, 1], region[:, 0], 0] = np.random.randint(low=100, high=256)
        img[region[:, 1], region[:, 0], 1] = np.random.randint(low=100, high=256)
        img[region[:, 1], region[:, 0], 2] = np.random.randint(low=100, high=256)
        return img

    ## 提取 MSER 连通区域（带标记,显示过程）
    def debug_extraction_with_labels(self, flt = None, direction = 0):
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








