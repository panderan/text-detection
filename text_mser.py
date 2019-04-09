## Libraries
import argparse
import os
import sys

import numpy as np
from PIL import Image
from scipy.stats import mode, norm

import cv2
import matplotlib.pyplot as plt
import progressbar
import pytesseract

IMAGE_PATH = "../data/YKT1.bmp"

## Parameters
AREA_LIM = 2.0e-4
PERIMETER_LIM = 1e-4
ASPECT_RATIO_LIM = 5.0
OCCUPATION_LIM = (0.23, 0.90)
COMPACTNESS_LIM = (3e-3, 1e-1)
KSIZE = 3
ITERATION = 7


## Displaying function
def pltShow(*images):
    count = len(images)
    nRow = np.ceil(count / 3.)
    for i in range(count):
        plt.subplot(nRow, 3, i + 1)
        if len(images[i][0].shape) == 2:
            plt.imshow(images[i][0], cmap='gray')
        else:
            plt.imshow(images[i][0])
        plt.xticks([])
        plt.yticks([])
        plt.title(images[i][1])
    plt.show()

class TextDetection(object):

    def __init__(self, image_path):
        self.imagaPath = image_path
        img = cv2.imread(image_path)
        rgbImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img = rgbImg
        self.final = rgbImg.copy()
        self.height, self.width = self.img.shape[:2]
        self.grayImg = cv2.cvtColor(self.img.copy(), cv2.COLOR_RGB2GRAY)
        self.cannyImg = self.applyCanny(self.img)
        self.timg = self.grayImg.copy()

    def getMSERegions(self, img):
        mser = cv2.MSER_create()
        # img = cv2.cvtColor(img.copy(), cv2.COLOR_RGB2GRAY)
        regions, bboxes = mser.detectRegions(img)
        return regions, bboxes

    def colorRegion(self, img, region):
        img[region[:, 1], region[:, 0], 0] = np.random.randint(low=100, high=256)
        img[region[:, 1], region[:, 0], 1] = np.random.randint(low=100, high=256)
        img[region[:, 1], region[:, 0], 2] = np.random.randint(low=100, high=256)
        return img

    def applyCanny(self, img, sigma=0.33):
        v = np.median(img)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        return cv2.Canny(img, lower, upper)

    def getRegionShape(self, region):
        return (max(region[:, 1]) - min(region[:, 1]), max(region[:, 0]) - min(region[:, 0]))

    def getRegionArea(self, region):
        return len(list(region))        ## Number of pixels

    def getRegionPerimeter(self, region):
        x, y, w, h = cv2.boundingRect(region)
        return len(np.where(self.cannyImg[y:y + h, x:x + w] != 0)[0])

    def getOccupyRate(self, region):
        return (1.0 * self.getRegionArea(region)) / (self.getRegionShape(region)[0] * self.getRegionShape(region)[1] + 1.0e-10)

    def getAspectRatio(self, region):
        return (1.0 * max(self.getRegionShape(region))) / (min(self.getRegionShape(region)) + 1e-4)

    def getCompactness(self, region):
        return (1.0 * self.getRegionArea(region)) / (1.0 * self.getRegionPerimeter(region) ** 2)

    def detect(self):
        self.res10 = np.zeros_like(self.img)
        boxRes = self.img.copy()

        regions, bboxes = self.getMSERegions(self.grayImg)

        bar = progressbar.ProgressBar(maxval=len(regions), widgets=[progressbar.Bar(marker='=', left='[', right=']'), ' ', progressbar.SimpleProgress()])
        bar.start()

        ## Coloring the regions
        for i, region in enumerate(regions):
            bar.update(i + 1)

            if self.getRegionArea(region) <= self.grayImg.shape[0] * self.grayImg.shape[1] * AREA_LIM:
                continue;

            if self.getRegionPerimeter(region) <= 2 * (self.grayImg.shape[0] + self.grayImg.shape[1]) * PERIMETER_LIM:
                continue;

            if self.getAspectRatio(region) >= ASPECT_RATIO_LIM:
                continue;

            if (self.getOccupyRate(region) <= OCCUPATION_LIM[0]) or (self.getOccupyRate(region) >= OCCUPATION_LIM[1]):
                continue;

            if (self.getCompactness(region) <= COMPACTNESS_LIM[0]) or (self.getCompactness(region) >= COMPACTNESS_LIM[1]):
                continue;

            self.res10 = self.colorRegion(self.res10, region)
            tbox = bboxes[i]
            x, y, w, h = cv2.boundingRect(region)
            self.timg = cv2.rectangle(self.timg, (x, y), (w, h), (255, 0, 0))
    
        bar.finish()

        ## Binarize regions
        binarized = np.zeros_like(self.grayImg)
        rows, cols, color = np.where(self.res10 != [0, 0, 0])
        binarized[rows, cols] = 255

        ## Dilate regions and find contours
        kernel = np.zeros((KSIZE, KSIZE), dtype=np.uint8)
        kernel[(KSIZE // 2)] = 1

        res = np.zeros_like(self.grayImg)
        dilated = cv2.dilate(binarized.copy(), kernel, iterations=ITERATION)
        image, contours, hierarchies = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i, (contour, hierarchy) in enumerate(zip(contours, hierarchies[0])):
            if hierarchy[-1] == -1:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(self.final, [box], 0, (0, 255, 0), 2)
                cv2.drawContours(res, [box], 0, 255, -1)

        return res

if IMAGE_PATH:
    td = TextDetection(IMAGE_PATH)
    res = td.detect()
    pltShow((td.img, "Original"), (td.final, "Final"), (res, "Mask"))
