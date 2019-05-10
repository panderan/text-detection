#!/usr/bin/env python

## @file main.py
# 将一幅输入的图像中的候选区域分别保存为图片
#   
# @author panderan@163.com 
#

from text_detection import mser, filter, morph, contours, svm, regions 
import matplotlib.pyplot as plt
import cv2
import sys


# 获取输入图片地址
IMAGE_PATH = sys.argv[1]
print("FILE:" + IMAGE_PATH)
 
# 启用 SVM 分类   
ENABLE_SVM = False
if len(sys.argv) > 2:
    if sys.argv[2] == "svm":
        ENABLE_SVM = True
    print("SVM: True")

# 创建 MSER 实例和几何过滤实例，提取 MSER 选区
msr = mser.mser_cls(IMAGE_PATH)
flt = filter.mser_filter400k()
binaries = msr.extraction_in_all_channel_with_labels(flt = flt)

# 对由候选区组成的二值图像进行形态学处理
mph = morph.morph()
binaries = mph.morph_operation(binaries)

# 创建选区处理实例，并从二值图像中提起候选区域分别保存为图片
ctr = contours.tdcontours(binaries, IMAGE_PATH.split('/')[-1][0:-4])
ctr.aggreate_contours_using_boxes()

text_regions_binaries = ctr.binaries.copy()
if ENABLE_SVM:
    classification = svm.svc()
    classification.train("IDCards/Rear/Training")
    text_regions_binaries = classification.filter_regions(msr.gray_img, ctr.binaries)

# ret_img = regions.regions.label_image(msr.gray_img, text_regions_binaries)
ret_img = regions.regions.label_image_with_box(msr.gray_img, ctr.boxes)
plt.imshow(ret_img, "gray")
plt.show()

