import cv2
import numpy as np
import matplotlib.pyplot as plt

class tdcontours:

    def __init__(self, binaries, name):
        self.binaries = binaries
        self.name = name

    def get_contours(self):
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    def get_contours_verbose(self):
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for item in contours:
            tmp = np.zeros_like(self.binaries)
            tmp[item[:,0,1], item[:,0,0]] = 1
            plt.ion()
            plt.imshow(tmp)
            plt.pause(1)

    def save_each_contours(self, orig_img):
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        retimg = np.zeros_like(orig_img)
        tmp = np.zeros_like(self.binaries)
        for i, (ctr, hiry) in enumerate(zip(contours, hierarchies[0])):
            if hiry[3] == -1:
                # Mask seg image
                mask = np.zeros_like(self.binaries)
                mask = cv2.drawContours(mask, [ctr], 0, 255, thickness=cv2.FILLED)
                x,y,w,h = cv2.boundingRect(ctr)
                mask_seg = mask[y:y+h, x:x+w]
                
                # seg image
                gray_img = np.zeros_like(self.binaries)
                gray_img[mask > 0] = orig_img[mask > 0]
                gray_img_seg = gray_img[ y:y+h, x:x+w]
                
                # show image
                ro_rect = cv2.minAreaRect(ctr)
                box = cv2.boxPoints(ro_rect)
                box = np.int0(box)
                bx,by,bw,bh = cv2.boundingRect(box)
                gray_img_copy = cv2.drawContours(gray_img.copy(), [box], 0, 255)
                
                # label and save
                plt.ion()
                plt.imshow(gray_img_copy[by:by+bh, bx:bx+bw], "gray")
                plt.pause(0.5)
                judge = input("is text region? : ")
                if (judge == 'Y'):
                    cv2.imwrite(self.name+"-"+str(i)+"-Y.jpg", gray_img_seg)
                    cv2.imwrite("mask/"+self.name+"-"+str(i)+"-Y-mask.jpg", mask_seg)
                else:
                    cv2.imwrite(self.name+"-"+str(i)+"-N.jpg", gray_img_seg)
                    cv2.imwrite("mask/"+self.name+"-"+str(i)+"-N-mask.jpg", mask_seg)



                # tmp[mask > 0] = orig_img[mask > 0]
                # cv2.drawContours(tmp, [box], 0, (255,255,255))
                # plt.ion()
                # plt.imshow(tmp, "gray")
                # plt.pause(1)
        # plt.ioff()
        # plt.imshow(tmp, "gray")
        # plt.show()


