#!/usr/bin/env python

## @file save_regions.py
# 将一幅输入的图像中的候选区域分别保存为图片
#   
# @author panderan@163.com 
#

from text_detection import mser, filter, morph, contours
import matplotlib.pyplot as plt
import cv2
import sys

# 获取输入图片地址
IMAGE_PATH = sys.argv[1]
SAVE_PATH = ""
if len(sys.argv) == 3:
    SAVE_PATH = sys.argv[2]

# 创建 MSER 实例和几何过滤实例，提取 MSER 选区
msr = mser.mser_cls(IMAGE_PATH)
flt = filter.mser_filter400k(msr.gray_img)
rect, binaries = msr.extraction_with_labels(flt = flt)

# 对由候选区组成的二值图像进行形态学处理
kl = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
binaries = cv2.dilate(binaries, kl)
binaries = morph.morph.closeing(binaries)

# 创建选区处理实例，并从二值图像中提起候选区域分别保存为图片
ctr = contours.tdcontours(binaries, IMAGE_PATH.split('/')[-1][0:-4], SAVE_PATH)
ctr.save_each_contours(msr.gray_img)


#plt.imshow(binaries)
#plt.show()
