import matplotlib.pyplot as plt
import numpy as np
import cv2

class graycluster:
    def __init__(self, grayImg):
        self.grayImg = grayImg
        self.width = grayImg.shape[1]
        self.height = grayImg.shape[0]

    def cluster(self, k):
       pixels = self.grayImg.reshape((self.width*self.height, 1))
       pixels = np.float32(pixels) 
       criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
       flags = cv2.KMEANS_RANDOM_CENTERS
       compactness,labels,centers = cv2.kmeans(pixels,k,None,criteria,10,flags)

       for i in range(0,k):
           pixels[labels==i] = centers[i]

       retGrayImg = pixels.reshape((self.height, self.width))
       return np.uint8(retGrayImg)

