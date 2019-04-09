import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

def strokeEdge(src, dst, blurKsize = 7, edgeKsize = 5):
    if blurKsize >= 3:
        blurredSrc = cv2.medianBlur(src, blurKsize)
        graySrc = cv2.cvtColor(blurredSrc, cv2.COLOR_BGR2GRAY)
    else:
        graySrc = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    cv2.Laplacian(graySrc, cv2.CV_8U, graySrc, ksize = edgeKsize)

    normalizedInverseAlpha = (1.0 / 255) * (255 - graySrc)
    channels = cv2.split(src)
    for channel in channels:
        channel[:] = channel * normalizedInverseAlpha

    cv2.merge(channels, dst)
    
    plt.subplot(121), plt.imshow(src)
    plt.subplot(122), plt.imshow(dst)
    plt.show()

img = cv2.imread("../../text-detection/images/scenetext01.jpg")
dst = np.zeros(img.shape, img.dtype)

strokeEdge(img, dst)
