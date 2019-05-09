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

## MSER 连通域提取类
#
# 从一幅灰度图像中提取 MSER 连通域
#
class mser_cls:
    
    ## 构造函数
    # 以灰度图像的形式读入图像，并保持其长宽比将其总像素数量缩放到400,000 左右
    # 
    # @param IMAGE_PATH 输入图像的路径
    def __init__(self, IMAGE_PATH):
        color_img = cv2.imread(IMAGE_PATH)
        b_img = color_img[:,:,0]
        g_img = color_img[:,:,1]
        r_img = color_img[:,:,2]
        gimg = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        mul = sqrt(gimg.shape[0]*gimg.shape[1]/400000)
        self.gray_img = cv2.resize(gimg, (int(gimg.shape[1]/mul), int(gimg.shape[0]/mul)))
        self.b_img = cv2.resize(b_img, (int(b_img.shape[1]/mul), int(b_img.shape[0]/mul)))
        self.g_img = cv2.resize(g_img, (int(g_img.shape[1]/mul), int(g_img.shape[0]/mul)))
        self.r_img = cv2.resize(r_img, (int(r_img.shape[1]/mul), int(r_img.shape[0]/mul)))
        self.delta = 5
        self.min_area = 9 
        self.max_area =500 
        self.variation = 0.25

    ## 提取 MSER 连通区域
    #
    # @param flt 几何条件过滤实例，为 0 则不过滤
    # @param direction MSER 提取方向，0 为 MSER+ ，1 为 MSER-
    #
    # @retval retmsrs 候选连通域列表，每一个元素为包含了该连通域的所有点的列表
    # @retval retboxes 候选连通域列表，每一个元素包含了该连通域的外接矩形
    #
    def extraction(self, flt = 0, direction = 0, channel="gray"):
        img = None
        if channel == "blue":
            img = self.b_img
        elif channel == "green":
            img = self.g_img
        elif channel == "red":
            img = self.r_img
        else:
            img = self.gray_img

        mser = cv2.MSER_create(_delta = self.delta, _min_area = self.min_area, _max_area = self.max_area)
        if direction == 0:
            msers, bboxes = mser.detectRegions(img)
        else:
            msers, bboxes = mser.detectRegions(255 - img)

        retmsrs = []
        retboxes = []
        if type(flt) != type(0):
            flt.set_image(img)
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

    ## 提取 MSER 连通区域（带标记）
    #
    # @param flt 几何条件过滤实例，为 0 则不过滤
    # @param direction MSER 提取方向，0 为 MSER+ ，1 为 MSER-
    #
    # @retval rect_img 在原图中用矩形标出候选区域图像
    # @retval binarized 以背景图像为0，提取的连通域为255 的二值图像
    #
    def extraction_with_labels(self, flt = 0, direction = 0, channel="gray"):
        rect_img = self.gray_img.copy()
        binarized = np.zeros_like(self.gray_img)
        msers, bboxes = self.extraction(flt, direction, channel)
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

    def extraction_in_all_channel_with_labels(self, flt = 0, direction = 0):
        grect, gbinaries = self.extraction_with_labels(flt = flt, channel="gray")
        b_rect, b_binaries = self.extraction_with_labels(flt = flt, channel="blue")
        g_rect, g_binaries = self.extraction_with_labels(flt = flt, channel="green")
        r_rect, r_binaries = self.extraction_with_labels(flt = flt, channel="red")
        gbinaries[b_binaries > 128] = b_binaries[b_binaries > 128]
        gbinaries[g_binaries > 128] = g_binaries[g_binaries > 128]
        gbinaries[r_binaries > 128] = r_binaries[r_binaries > 128]
        return gbinaries


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

