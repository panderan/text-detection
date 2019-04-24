#!/usr/bin/env python

## @package text_detection
#   
# @file morph.py
# 图像形态学处理
#   
# @author panderan@163.com 
#

import cv2

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
