import cv2
import numpy as np
import matplotlib.pyplot as plt

class tdcontours:

    def __init__(self, binaries):
        self.binaries = binaries

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
                mask = np.zeros_like(self.binaries)
                # tmp[ctr[:,0,1], ctr[:,0,0]] = 255
                rect = cv2.minAreaRect(ctr)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # cv2.drawContours(tmp, [box], 0, (255,255,255))
                cv2.fillPoly(mask,[box], (255,255,255))
                tmp[mask > 0] = orig_img[mask > 0]
                plt.ion()
                plt.imshow(tmp, "gray")
                plt.pause(1)
        plt.ioff()
        plt.imshow(tmp, "gray")
        plt.show()


            # box = cv2.boxPoints(rect)
            # xs = np.int32(np.sort(np.unique(box[:,0])))
            # ys = np.int32(np.sort(np.unique(box[:,1])))
            # tmp[ys[0]:ys[1], xs[0]:xs[1]] = 255
        #     rect = cv2.minAreaRect(item)
        #     box = cv2.boxPoints(rect)
        #     xs = np.int32(np.sort(np.unique(box[:,0])))
        #     ys = np.int32(np.sort(np.unique(box[:,1])))
        #     w = xs[1] - xs[0]
        #     h = ys[1] - ys[0]
        #     retimg[ys[0]:ys[1] , xs[0]:xs[1]] = orig_img[ys[0]:ys[1] , xs[0]:xs[1]]

            # rect = cv2.minAreaRect(item)
            # box = cv2.boxPoints(rect)
            # xs = np.int32(np.sort(np.unique(box[:,0])))
            # ys = np.int32(np.sort(np.unique(box[:,1])))
            # w = xs[1] - xs[0]
            # h = ys[1] - ys[0]
            # tmp = np.ndarray((h,w))
            # tmp[:,:] = orig_img[ys[0]:ys[1], xs[0]:xs[1]]
            # plt.ion()
            # plt.imshow(tmp)
            # plt.pause(1)

