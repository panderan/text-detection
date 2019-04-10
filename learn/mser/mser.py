import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import pause
import filter


# 读取图像
img1 = cv2.imread("../../../data/YKT1.bmp")
img2 = cv2.imread("../../../data/PAN.bmp")
img = img1.copy()
grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
v = np.median(img)
lower = int(max(0, (1.0 - 0.33) * v))
upper = int(min(255, (1.0 + 0.33) * v))
edgesImg = cv2.Canny(grayImg, lower, upper)
binarized = np.zeros_like(grayImg)
ft800 = filter.mser_filter800(grayImg)

# MSER 提取
mser = cv2.MSER_create()
msers, bboxes = mser.detectRegions(grayImg)

# 过滤 MSER 选区
retImg = grayImg.copy()
for i,box in enumerate(bboxes):
    if ft800.verification(retImg, msers[i], box):
        retImg = cv2.rectangle(retImg, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
        binarized[ msers[i][:, 1], msers[i][:, 0]] = 255

plt.imshow(binarized)
plt.show()

