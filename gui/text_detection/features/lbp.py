#!/usr/bin/env python

## @package text_detection
#   
# @file lbp.py
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
from text_detection import common


class lbp:

    def __init__(self, points=8, radius=1):
        self.number_points = points
        self.radius = radius

    def get_lbp_feature(self, gimg, gimg_msk):
        gimg = common.common.zoom(gimg, 100000)
        gimg_msk = cv2.resize(gimg_msk, (gimg.shape[1], gimg.shape[0]))

        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        lbp[gimg_msk <127] = 256
        data = lbp.ravel()
        data = data[data<256]
        y,x =np.histogram(data, range(0,256+1)) 
        
        # 旋转不变值
        idx = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 37, 39, 43, 45, 47, 51, 53, 55, 59, 61, 63, 85, 87, 91, 95, 111, 119, 127, 255]
        y = [y[i] for i in idx]
        y = y/sum(y)

        return y
    
    def get_training_data(self, dir):

        training_datas = []
        labels = []
        
        # 遍历目录
        for root, dirs, files in os.walk(dir, topdown=True):
            # 目标根目录
            if root==dir:
                # 遍历目标根目录下的每一个文件
                for filename in files:

                    # 匹配文件名后缀
                    if re.search('[jpg|png]$', filename):
                        
                        # 构建目标文件名以及目标mask文件名
                        filepath = os.path.join(root, filename)
                        msk_filepath = filepath.split('/')
                        msk_filepath.insert(-1, "mask")
                        msk_filepath[-1] = (msk_filepath[-1])[0:-4] + "-mask" + (msk_filepath[-1][-4:])
                        msk_filepath = '/'.join(msk_filepath)
                        
                        # 获取 LBP 特征
                        img = cv2.imread(filepath, 0)
                        img = common.common.zoom(img, 100000)
                        msk_img = cv2.imread(msk_filepath, 0)
                        msk_img = cv2.resize(msk_img, (img.shape[1], img.shape[0]))

                        feature_vector = self.get_lbp_feature(img, msk_img)
                        training_datas.append(feature_vector)

                        # 获取 Label
                        if filepath[-5] == 'Y':
                            labels.append('Y')
                        elif filepath[-5] == 'N':
                            labels.append('N')

        return (training_datas, labels)                     

