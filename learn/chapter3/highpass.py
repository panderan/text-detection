import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

kernel_3x3 = np.array([ [-1, -1, -1],
                        [-1,  8, -1],
                        [-1, -1, -1]
                        ])

kernel_5x5 = np.array([ [-1, -1, -1, -1, -1],
                        [-1,  1,  2,  1, -1],
                        [-1,  2,  4,  2, -1],
                        [-1,  1,  2,  1, -1],
                        [-1, -1, -1, -1, -1]
                        ])

img = cv2.imread("../../text-detection/images/scenetext01.jpg", 0)
k3 = ndimage.convolve(img, kernel_3x3)
k5 = ndimage.convolve(img, kernel_5x5)

blurred = cv2.GaussianBlur(img, (11,11), 0)
g_hpf = img - blurred

plt.subplot(221), plt.imshow(img)
plt.subplot(222), plt.imshow(k3)
plt.subplot(223), plt.imshow(k5)
plt.subplot(224), plt.imshow(g_hpf)
plt.show()
