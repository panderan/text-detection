#!/usr/bin/env python

## @package text_detection
#   
# @file cluster.py
# 像素灰度值聚类
#   
# @author panderan@163.com 
#

import matplotlib.pyplot as plt
import numpy as np
import cv2

## 像素灰度值聚类类
#
class graycluster:
    
    ## 构造函数
    def __init__(self, grayImg):
        self.grayImg = grayImg
        self.width = grayImg.shape[1]
        self.height = grayImg.shape[0]
    
    ## Kmean 聚类
    #
    # @param k 聚类中心个数
    # @retval img 聚类后的图像
    #
    def kmeans(self, k):
       pixels = self.grayImg.reshape((self.width*self.height, 1))
       pixels = np.float32(pixels) 
       criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
       flags = cv2.KMEANS_RANDOM_CENTERS
       compactness,labels,centers = cv2.kmeans(pixels,k,None,criteria,10,flags)

       for i in range(0,k):
           pixels[labels==i] = centers[i]

       retGrayImg = pixels.reshape((self.height, self.width))
       return np.uint8(retGrayImg)

