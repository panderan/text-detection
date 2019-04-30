import math
import cv2

class common:
    
    def __init__(self):
        pass
    
    @staticmethod
    def zoom(gimg, tgtsize):
        times = math.sqrt(gimg.shape[0]*gimg.shape[1]/tgtsize)
        gimg = cv2.resize(gimg, (int(gimg.shape[1]/times), int(gimg.shape[0]/times)))
        return gimg


























