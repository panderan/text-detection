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
        pass

    ## 开运算
    #
    # @param bins 输入的二值图像
    # @retval reimg 处理后的图像
    #
    def opening(bins):
        ubit = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        reimg = cv2.dilate(cv2.erode(bins, ubit), ubit)
        return reimg
    
    ## 闭运算
    #
    # @param bins 输入的二值图像
    # @retval reimg 处理后的图像
    #
    def closeing(bins):
        ubit = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        reimg = cv2.erode(cv2.dilate(bins, ubit), ubit)
        return reimg


    def morph_operation(self, binaries):
        image, contours, hierarchies = cv2.findContours(binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        ret_bins = np.zeros_like(binaries)

        for i, ctr in enumerate(contours):
            temp_binaries = np.zeros_like(binaries)
            temp_binaries = cv2.drawContours(temp_binaries, [ctr], 0, 255, thickness=cv2.FILLED)
            temp_binaries = self.morph_operation_once(temp_binaries)
            ret_bins[temp_binaries > 128] = temp_binaries[temp_binaries > 128] 

        return ret_bins

    def morph_operation_once(self, binaries):
        k1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        k2 = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))

        bins = cv2.erode(binaries, k1)
        if np.sum(bins) < 255:
            bins = binaries

        binaries = cv2.dilate(binaries, k2)
        binaries = morph.closeing(binaries)
        binaries = morph.opening(binaries)
        return binaries















