import matplotlib.pyplot as plt
from skimage import feature
import numpy as np
import os
import cv2
import math


def takeFirst(elem):
    return elem[0]


class dlbp_feature:

    def __init__(self, points=8, radius=1):
        self.number_points = points
        self.radius = radius

    def get_lbp_img(self, gray_img):
        lbp = feature.local_binary_pattern(gray_img, self.number_points, self.radius, method="ror")
        return lbp

    def get_dlbp_feature(self, gray_img):
        # lbp = self.get_lbp_img(gray_img)
        pass


class dlbp_training:

    def __init__(self, points=8, radius=1, occupied=0.8):
        self.number_points = points
        self.radius = radius
        self.occupied = occupied
        pass

    def training_k(self, dir):
        for root, dirs, files in os.walk(dir, topdown=True):
            if root==dir:
                k = 0.0
                for filename in files:
                    k += self.get_k(os.path.join(root, filename))
                k = k / len(files)
                return k
        return pow(2,self.points)

    def get_k(self, filename):
        # 获得 filename 和 msk_filename 文件的路径
        msk_filename = filename.split('/')
        msk_filename.insert(-1, "mask")
        msk_filename[-1] = (msk_filename[-1])[0:-4] + "-mask" + (msk_filename[-1][-4:-1]) + msk_filename[-1][-1]
        msk_filename = '/'.join(msk_filename)
        
        # 打开两个文件
        gimg = cv2.imread(filename, 0)
        gimg_msk = cv2.imread(msk_filename, 0)

        # 提取 gimg 文件 lbp
        lbp = feature.local_binary_pattern(gimg, self.number_points, self.radius, method="ror")
        lbp[gimg_msk <127] = 256
        data = lbp.ravel()
        data = data[data<256]
        x, y =np.histogram(data, range(0,256+1)) 
        x = x.tolist()
        x.sort(reverse=True)

        acc = 0
        for i,item in enumerate(x):
            acc += item
            if acc/sum(x) > self.occupied:
                return i

        






