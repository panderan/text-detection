#!/usr/bin/env python

''' 共用函数
'''

import cv2
import numpy as np

def uniform_illumination(gray_image):
    ''' 均匀光照
    '''
    b_mean = gray_image.mean()
    ksize = 32

    new_row = int(gray_image.shape[0]/ksize)
    new_col = int(gray_image.shape[1]/ksize)

    adj_mat = np.zeros([new_row, new_col])
    for i in range(new_row):
        for j in range(new_col):
            sub_image = gray_image[ksize*i:ksize*(i+1)-1, ksize*j:ksize*(j+1)-1]
            adj_mat[i, j] = sub_image.mean()

    adj_mat = adj_mat - b_mean
    adj_mat = cv2.resize(adj_mat, (gray_image.shape[1], gray_image.shape[0]))
    result = gray_image - adj_mat
    return np.uint8(result)


def apply_canny(gray_img, sigma=0.33):
    v = np.median(gray_img)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    return cv2.Canny(gray_img, lower, upper)
