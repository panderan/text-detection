#!/usr/bin/env python

## @package text_detection
#   
# @file contours.py
# 提取连通域边界模块
#   
# @author panderan@163.com 
#

import cv2
import numpy as np
import matplotlib.pyplot as plt

## 边界处理类
#
# 用于从二值图像中取得连通域边界
#
class tdcontours:
    
    ## 构造函数
    #
    # @param binaries 输入的二值图像
    # @param name 文件名
    #
    def __init__(self, binaries, name, save_path=""):
        self.binaries = binaries
        self.name = name
        self.save_path = save_path
        if len(self.save_path) > 0:
            if self.save_path[-1] != '/':
                self.save_path += '/'

    ## 获取轮廓
    # 直接调用 cv2.findContours 方法
    #
    def get_contours(self):
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return (image, contours, hierarchies)

    ## 获取轮廓
    # 直接调用 cv2.findContours 方法,结果可视
    #
    def get_contours_verbose(self):
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for item in contours:
            tmp = np.zeros_like(self.binaries)
            tmp[item[:,0,1], item[:,0,0]] = 1
            plt.ion()
            plt.imshow(tmp)
            plt.pause(1)

    ## 将每一个候选区域存为图像文件
    # 将每一个候选区域交互保存为图像文件，并在过程中人为交互标记该候选区是否是文字区域
    #
    # @param orig_img 原图
    #
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
                    cv2.imwrite(self.save_path + self.name+"-"+str(i)+"-Y.jpg", gray_img_seg)
                    cv2.imwrite(self.save_path + "mask/"+self.name+"-"+str(i)+"-Y-mask.jpg", mask_seg)
                else:
                    cv2.imwrite(self.save_path + self.name+"-"+str(i)+"-N.jpg", gray_img_seg)
                    cv2.imwrite(self.save_path + "mask/"+self.name+"-"+str(i)+"-N-mask.jpg", mask_seg)


