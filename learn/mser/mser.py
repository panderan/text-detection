import cv2
import matplotlib.pyplot as plt
import numpy as np

def getArea(region):
    return len(region)

def getPerimeter(box):
    tmp = edgesImg[box[0]:box[0]+box[2], box[1]:box[1]+box[3]]
    return len(np.where(tmp != 0)[0])
    
def getAspectRatio(region):
    h = max(region[:, 1]) - min(region[:, 1])
    w = max(region[:, 0]) - min(region[:, 0])
    return float(w) / float(h)

def getOccurpiedRatio(region, box):
    return float(getArea(region)) / (float(box[2]) * float(box[3]))

def getCompactness(region, box):
    return float(getArea(region)) / float(getPerimeter(box)**2)




img = cv2.imread("/Users/panderan/Documents/PythonEnv/mserocr/data/YKT1.bmp")
grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
v = np.median(img)
lower = int(max(0, (1.0 - 0.33) * v))
upper = int(min(255, (1.0 + 0.33) * v))
edgesImg = cv2.Canny(grayImg, lower, upper)

mser = cv2.MSER_create()
msers, bboxes = mser.detectRegions(grayImg)

retImg = grayImg.copy()
for i,box in enumerate(bboxes):
    # 面积
    retval = getArea(msers[i])
    if retval < img.shape[0]*img.shape[1]*0.0002:
        continue

    # 周长
    retval = getPerimeter(box)
    if retval <  2 * (img.shape[0] + img.shape[1]) * 0.0001:
        continue

    # 横纵比
    retval = getAspectRatio(msers[i])
    if retval > 5.0:
        continue

    # 占用率
    retval = getOccurpiedRatio(msers[i], box)
    if retval < 0.23 or retval > 0.9:
        continue

    # 紧密度
    retval = getCompactness(msers[i], box)
    if retval < 0.003 or retval > 0.1:
        continue

    print(i)
    retImg = cv2.rectangle(retImg, (box[0], box[1]), (box[2], box[3]), (255, 0, 0))

plt.imshow(retImg)
plt.show()
