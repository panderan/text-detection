from text_detection import dlbp
from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
import cv2

class svc:
    
    def __init__(self):
        self.trained = False
        self.dlbp_ft = None
        self.svc = None

    def train(self, datapath):

        # 构建 DLBP 描述实例
        self.dlbp_ft = dlbp.dlbp_feature()
        k, vtr, labels = self.dlbp_ft.training_k(datapath)
        training_data = np.array(vtr)[:, 0:self.dlbp_ft.k]
        
        # 构建 SVC 分类实例
        self.svc = svm.SVC(gamma='scale', kernel='poly', degree=50)
        self.svc.fit(training_data, labels)

        self.trained = True
    

    def filter_regions(self, gimg, boxes, debug = False):
        ret_boxes = []
        if self.trained == False:
            return boxes 

        for i, box in enumerate(boxes):
            # Mask seg image
            mask = np.zeros_like(gimg)
            mask = cv2.drawContours(mask, [box], 0, 255, thickness=cv2.FILLED)
            x,y,w,h = cv2.boundingRect(box)
            mask_seg = mask[y:y+h, x:x+w]
                 
            # seg image
            gray_img = np.zeros_like(gimg)
            gray_img[mask > 0] = gimg[mask > 0]
            gray_img_seg = gray_img[ y:y+h, x:x+w]
                
            # SVM 分类
            vet = self.dlbp_ft.get_dlbp_feature(gray_img_seg, mask_seg)
            pre = self.svc.predict(np.array(vet).reshape(1,-1))

            if str(pre[0]) == "Y":
                ret_boxes.append(box)

            if debug:
                print("Ret: " + pre[0])
                plt.subplot(121)
                plt.imshow(gray_img_seg, "gray")
                plt.subplot(122)
                plt.imshow(mask_seg, "gray")
                plt.show()

        return ret_boxes

