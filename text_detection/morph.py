#!/usr/bin/env python

## @package text_detection
#   
# @file morph.py
# 图像形态学处理
#   
# @author panderan@163.com 
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

## 图像形态学处理类
#
class morph:
    ## 构造函数
    def __init__(self):
        self.k_erode = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        self.k_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
        self.k_opening = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        self.k_closing = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        pass

    ## 开运算
    #
    # @param bins 输入的二值图像
    # @retval reimg 处理后的图像
    #
    def opening(self, bins):
        reimg = cv2.dilate(cv2.erode(bins, self.k_opening), self.k_opening)
        return reimg
    
    ## 闭运算
    #
    # @param bins 输入的二值图像
    # @retval reimg 处理后的图像
    #
    def closing(self, bins):
        reimg = cv2.erode(cv2.dilate(bins, self.k_closing), self.k_closing)
        return reimg

    ## 对输入的二值图像进行形态学处理
    #
    # 对二值图像中的每一个连通域进行先腐蚀后膨胀，如果腐蚀后连通域消失则略过
    # 腐蚀操作。然后进行闭运算和开运算
    #
    def morph_operation(self, binaries, debug = False):
        image, contours, hierarchies = cv2.findContours(binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        ret_bins = np.zeros_like(binaries)

        for i, ctr in enumerate(contours):
            temp_binaries = np.zeros_like(binaries)
            temp_binaries = cv2.drawContours(temp_binaries, [ctr], 0, 255, thickness=cv2.FILLED)
            temp_binaries = self._morph_operation_once(temp_binaries)
            if debug:
                tmp = ret_bins.copy()
                tmp[temp_binaries > 128] = 128
                cv2.namedWindow("Debug",0);
                cv2.resizeWindow("Debug", 800, 600);
                cv2.imshow("Debug", tmp)
                cv2.waitKey(0)
            ret_bins[temp_binaries > 128] = temp_binaries[temp_binaries > 128] 

        return ret_bins

    ## 对输入的二值图像进行形态学处理，只处理一个连通域
    #
    def _morph_operation_once(self, binaries, debug = False):
        
        if debug:
            cv2.namedWindow("Debug",0);
            cv2.resizeWindow("Debug", 800, 600);
            cv2.imshow("Debug", binaries)
            cv2.waitKey(1)
        
        bins = cv2.erode(binaries, self.k_erode)

        image, contours, hierarchies = cv2.findContours(bins, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 1:
            bins = binaries

        before_size = np.sum(binaries)/255.0
        after_size = np.sum(bins)/255.0
        if after_size < 1.0:
            bins = binaries
        elif after_size/before_size < 1.0/9.0:
            bins = binaries
        
        if before_size < 500:
            bins = cv2.dilate(bins, self.k_dilate)
        bins = self.closing(bins)
        bins = self.opening(bins)
        return bins

    @property
    def k_dilate(self):
        return self.__k_dilate
    @k_dilate.setter
    def k_dilate(self, val):
        self.__k_dilate = val

    @property
    def k_erode(self):
        return self.__k_erode
    @k_erode.setter
    def k_erode(self, val):
        self.__k_erode = val

    @property
    def k_opening(self):
        return self.__k_opening
    @k_opening.setter
    def k_opening(self, val):
        self.__k_opening = val

    @property
    def k_closing(self):
        return self.__k_closing
    @k_closing.setter
    def k_closing(self, val):
        self.__k_closing = val








