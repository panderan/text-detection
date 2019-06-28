#!/usr/bin/env python

## @package text_detection
#   
# @file dlbp.py
# 提取选区 DLBP 特征类
# 
# @author panderan@163.com 
#

import matplotlib.pyplot as plt
from skimage import feature
import numpy as np
import os
import cv2
import math
import re

## 返回二元组的第一个元素
#
def takeFirst(elem):
    return elem[0]


## DLBP 特征训练类
# 用以获取参数 K 的大小
#
class dlbp_training:
    
    ## 构造函数
    #
    # @param points 采样点个数
    # @param radius 采样范围半径
    # @param occupied 主要特征占有率
    #
    def __init__(self, points=8, radius=1, occupied=0.9):
        self.number_points = points
        self.radius = radius
        self.occupied = occupied
        self.k = 0
        pass

    ## 见 DLBP Algorithm 2
    #
    def training_k(self, dir):
        vtrs = []
        labels = []
        for root, dirs, files in os.walk(dir, topdown=True):
            if root==dir:
                k = 0.0
                for filename in files:
                    if re.search('[jpg|png]$', filename):
                        i,x = self.get_k(os.path.join(root, filename))
                        k+=i
                        vtrs.append(x)
                        if filename[-5] == 'Y':
                            labels.append('Y')
                        elif filename[-5] == 'N':
                            labels.append('N')
                k = k / len(files)
                self.k = np.int0(k+0.5)
                return (k,vtrs,labels)

    ## 见 DLBP Algorithm 1
    #
    def get_k(self, filename):
        
        # 提取 gimg 文件 lbp
        gimg = cv2.imread(filename, 0)
        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        data = lbp.ravel()
        x, y =np.histogram(data, range(0,256+1)) 
        x = x.tolist()
        x.sort(reverse=True)

        acc = 0
        for i,item in enumerate(x):
            acc += item
            total = sum(x)
            if acc/total > self.occupied:
                return (i, x)


## DLBP 特征提取类
# DLBP 特征提取前，需要先训练参数k
#
class dlbp_feature(dlbp_training):

    ## 构造函数
    # 参数同父类
    #
    def __init__(self, points=8, radius=1, occupied=0.85):
        super(dlbp_feature, self).__init__(points, radius, occupied)

    ## 获取 DLBP 图像
    #
    # @param gimg 输入的待提取特征的图像
    #
    def get_lbp_img(self, gimg):
        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        return lbp

    ## 获取 DLBP 特征
    #
    # @param gimg 输入的待提取特征的图像
    # @param gimg_msk 输入的待提取特征的图像的掩码图
    #
    def get_dlbp_feature(self, gimg):
        if self.k == 0:
            print("DLBP need training first\n")
            return None
        
        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        data = lbp.ravel()
        x, y =np.histogram(data, range(0,256+1)) 
        x = x.tolist()
        total = sum(x)
        x.sort(reverse=True)
        return np.array(x[:self.k])


