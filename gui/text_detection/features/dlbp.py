#!/usr/bin/env python

'''
# 提取选区 DLBP 特征类
'''
import os
import re
import numpy as np
import cv2
from skimage import feature


def takeFirst(elem):
    ''' 返回二元组的第一个元素
    '''
    return elem[0]


class TdFeatureTrainingDLBP:
    ''' DLBP 特征训练类
        用以获取参数 K 的大小
    '''
    def __init__(self, points=8, radius=1, occupied=0.9):
        ''' 构造函数
        Args:
            points 采样点个数
            radius 采样范围半径
            occupied 主要特征占有率
        '''
        self.number_points = points
        self.radius = radius
        self.occupied = occupied
        self.k = 0
        self.k_c = 3

    def training_k(self, dirpath):
        ''' 见 DLBP Algorithm 2
        '''
        k = None
        vtrs = []
        labels = []
        for root, _, files in os.walk(dirpath, topdown=True):
            if root == dirpath:
                k = 0.0
                for filename in files:
                    if re.search('[jpg|png]$', filename):
                        i, x = self.getK(os.path.join(root, filename))
                        k += i
                        vtrs.append(x)
                        if filename[-5] == 'Y':
                            labels.append('Y')
                        elif filename[-5] == 'N':
                            labels.append('N')
                k = k / len(files)
                self.k = np.int0(k+0.5) + self.k_c
                break
        return (k, vtrs, labels)

    def getK(self, filename):
        ''' 见 DLBP Algorithm 1
        '''
        # 提取 gimg 文件 lbp
        gimg = cv2.imread(filename, 0)
        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        data = lbp.ravel()
        x, y = np.histogram(data, range(0, 256+1))
        x = x.tolist()
        x.sort(reverse=True)

        acc = 0
        for i, item in enumerate(x):
            acc += item
            total = sum(x)
            if acc/total > self.occupied:
                return (i, x)


class TdFeatureDLBP(TdFeatureTrainingDLBP):
    ''' DLBP 特征提取类
        DLBP 特征提取前，需要先训练参数 k
    '''
    def __init__(self, points=8, radius=1, occupied=0.85):
        super().__init__(points, radius, occupied)

    def getLBPImage(self, gimg):
        ''' 获取 DLBP 图像
        Args:
            gimg 输入的待提取特征的图像
        '''
        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        return lbp

    def getDLBP(self, gimg):
        ''' 获取 DLBP 特征
        Args:
            gimg 输入的待提取特征的图像
            gimg_msk 输入的待提取特征的图像的掩码图
        '''
        if self.k == 0:
            print("DLBP need training first\n")
            return None

        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        data = lbp.ravel()
        x, y = np.histogram(data, range(0, 256+1))
        x = x.tolist()
        x.sort(reverse=True)
        return np.array(x[:self.k])
