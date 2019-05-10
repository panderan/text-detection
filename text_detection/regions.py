import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

class regions:
    
    def __init__(self):
        pass
    
    @staticmethod
    def label_image(img, mask):
        ret_img = img.copy()
        image, contours, hierarchies = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        for i, (ctr, hiry) in enumerate(zip(contours, hierarchies[0])):
            ret_img = cv2.drawContours(ret_img, [ctr], 0, (255,255,255))
        return ret_img

    @staticmethod
    def label_image_with_box(img, boxes):
        ret_img = img.copy()
        for i,box in enumerate(boxes):
            ret_img = cv2.drawContours(ret_img, [np.int0(box)], 0, 255, thickness=1)
        return ret_img

