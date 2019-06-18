import math
import cv2
import numpy as np

class common:
    
    def __init__(self):
        pass
    
    @staticmethod
    def zoom(gimg, tgtsize):
        times = math.sqrt(gimg.shape[0]*gimg.shape[1]/tgtsize)
        gimg = cv2.resize(gimg, (int(gimg.shape[1]/times), int(gimg.shape[0]/times)))
        return gimg

    @staticmethod
    def unevenLightCompensate(gray, blockSize = 3):

        average = np.mean(gray)
        rows_new = int(np.ceil(gray.shape[0] / blockSize))
        cols_new = int(np.ceil(gray.shape[1] / blockSize))

        blockImage = np.zeros((rows_new, cols_new), dtype=np.float32)
        for r in range(rows_new):
            for c in range(cols_new):
                rowmin = r * blockSize
                rowmax = (r + 1) * blockSize
                if (rowmax > gray.shape[0]):
                    rowmax = gray.shape[0]
                colmin = c * blockSize
                colmax = (c + 1) * blockSize
                if (colmax > gray.shape[1]):
                    colmax = gray.shape[1]

                imageROI = gray[rowmin:rowmax, colmin:colmax]
                temaver = np.mean(imageROI)
                blockImage[r, c] = temaver

        blockImage = blockImage - average
        blockImage2 = cv2.resize(blockImage, (gray.shape[1], gray.shape[0]), interpolation=cv2.INTER_CUBIC)
        gray2 = gray.astype(np.float32)
        dst = gray2 - blockImage2
        dst = dst.astype(np.uint8)
        dst = cv2.GaussianBlur(dst, (3, 3), 0)

        return dst
























