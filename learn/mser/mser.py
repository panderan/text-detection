import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import pause
import filter
import cluster

# 读取图像
img1 = cv2.imread("../../../data/YKT1.bmp")
img2 = cv2.imread("../../../data/PAN.bmp")
img3 = cv2.imread("./clustered.jpg")
img = img1.copy()

# 颜色聚类
grayImg256 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
grayImg = grayImg256
# cr = cluster.graycluster(grayImg256)
# grayImg = cr.cluster(16)

# 提取边缘
v = np.median(grayImg256)
lower = int(max(0, (1.0 - 0.33) * v))
upper = int(min(255, (1.0 + 0.33) * v))
edgesImg = cv2.Canny(grayImg256, lower, upper)
binarized = np.zeros_like(grayImg256)

# MSER 提取
mser = cv2.MSER_create()
msers, bboxes = mser.detectRegions(grayImg256)

# 过滤 MSER 选区
retImg = grayImg.copy()
ft800 = filter.mser_filter800(grayImg)
for i,box in enumerate(bboxes):
    if ft800.verification(retImg, msers[i], box):
        retImg = cv2.rectangle(retImg, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
        binarized[ msers[i][:, 1], msers[i][:, 0]] = 255

plt.imshow(binarized)
plt.show()

