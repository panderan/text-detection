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


    @staticmethod
    def get_region_aspect_ratio(region, gt1=False):

        box = np.int0(cv2.boxPoints(cv2.minAreaRect(region)))
        return common.get_box_aspect_ratio(box, gt1)


    @staticmethod
    def get_box_aspect_ratio(box, gt1=False):

        p0=np.array(box[-1])
        p1=np.array(box[0])
        p2=np.array(box[1])
        h=l1=p1-p0
        w=l2=p1-p2
        
        if (l1[0] == 0 and l1[1] == 0)\
            or (l2[0] == 0 and l2[1] == 0):
            return 9999

        angle = math.asin(l1[1]/math.hypot(l1[0],l1[1]))
        if angle > -math.pi/4 and angle < math.pi/4:
            w=l1
            h=l2    

        dw=math.hypot(w[0],w[1])+1
        dh=math.hypot(h[0],h[1])+1

        ratio = dw/dh
        if gt1 and ratio < 1.0:
            ratio = 1.0 / ratio

        return ratio,dw,dh


    @staticmethod
    def get_box_direction(box):
        h = box[0] - box[1]
        v = box[2] - box[1]
        dh=math.hypot(h[0],h[1])
        dv=math.hypot(v[0],v[1])

        if dh > dv:
            d = h*[1,-1]
        else: 
            d = v*[1,-1]
        return math.asin(d[1]/math.hypot(d[0],d[1]))


    @staticmethod
    def get_box_area(box):
        p0=np.array(box[0])
        p1=np.array(box[1])
        p2=np.array(box[2])
        l1=p1-p0
        l2=p1-p2
        d1=math.hypot(l1[0],l1[1])
        d2=math.hypot(l2[0],l2[1])
        return d1*d2,d1,d2
















