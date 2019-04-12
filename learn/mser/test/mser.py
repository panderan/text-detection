import cv2
import matplotlib.pyplot as plt
import numpy as np

delta = 5

# 读取图像
img = cv2.imread("test4.jpg", 0)

# MSER 提取
mser = cv2.MSER_create(_delta=delta, _min_area=60, _max_area=40000)
msers, bboxes = mser.detectRegions(img)

# 绘制 MSER 选区
retImg = img.copy()
binarized = np.zeros_like(img)
regionArea = [0]*256
selectArea = [0]*256

for i,box in enumerate(bboxes):
        # 每一个选区
        one = img.copy()
        one = cv2.rectangle(one, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
        one[ msers[i][:, 1], msers[i][:, 0]] = 255
        cv2.imwrite("everyRegion/region" + str(i) + ".jpg", one)

        retImg = cv2.rectangle(retImg, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
        binarized[ msers[i][:, 1], msers[i][:, 0]] = 255
        selectArea[i] = len(msers[i])

# 绘制所有阈值
for i in range(0,256):
    th, bin = cv2.threshold(img, i, 255, cv2.THRESH_BINARY)
    regionArea[i] = (bin == 0).sum()

plt.subplot(121)
plt.imshow(binarized)
plt.subplot(122)
plt.imshow(retImg), plt.show() 
