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
import math

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
    def save_each_contours(self, orig_img, save=True):
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        # retimg = np.zeros_like(orig_img)
        retimg = orig_img.copy()
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
                retimg = cv2.drawContours(retimg, [box], 0, 255)
                
                # label and save
                if save==True:
                    plt.ion()
                    plt.imshow(gray_img_copy[by:by+bh, bx:bx+bw], "gray")
                    plt.pause(0.2)
                    judge = input("is text region? : ")
                    if (judge == 'Y'):
                        cv2.imwrite(self.save_path + self.name+"-"+str(i)+"-Y.jpg", gray_img_seg)
                        cv2.imwrite(self.save_path + "mask/"+self.name+"-"+str(i)+"-Y-mask.jpg", mask_seg)
                    else:
                        cv2.imwrite(self.save_path + self.name+"-"+str(i)+"-N.jpg", gray_img_seg)
                        cv2.imwrite(self.save_path + "mask/"+self.name+"-"+str(i)+"-N-mask.jpg", mask_seg)
        return retimg

    def aggreate_contours(self):
        num1 = self.aggreate_contours_once()
        numx = self.aggreate_contours_once()
        while (numx != num1):
            num1 = numx
            numx = self.aggreate_contours_once()
        self.delsmallregions()
         

    def aggreate_contours_once(self):
        boxes = []
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i, ctr in enumerate(contours):
            ro_rect = cv2.minAreaRect(ctr)
            box = np.int0(cv2.boxPoints(ro_rect))
            # downleft = self.getDownleftPnt(box)
            # upleft = self.getUpleftPnt(box)
            # upright = self.getUprightPnt(box)
            downleft = box[0]
            upleft = box[1] 
            upright = box[2] 
            areasize = self.boxPointsArea(box)
            direction = self.boxDirection(np.array(upleft), np.array(upright), np.array(downleft))
            aspectratio = self.boxAspectRatio(np.array(upleft), np.array(upright), np.array(downleft))
            boxes.append((box, upleft, upright, downleft, areasize, direction, aspectratio))

        lines_img = np.zeros_like(self.binaries)
        tmp = self.binaries.copy()
        retflag = False
        for i,boxa in enumerate(boxes):
            for boxb in boxes[i+1:]:
                bbox_points = np.int0(np.array(boxa[0].tolist()+boxb[0].tolist()))
                bbox = cv2.boxPoints(cv2.minAreaRect(bbox_points))
                 
                # Debug
                print(retflag)
                # cv2.imshow("ddd", tmp)
                # cv2.waitKey(0)
                retflag = False
                tmp = self.binaries.copy()
                tmp = cv2.drawContours(tmp, [boxa[0]], 0, 128, thickness=cv2.FILLED)
                tmp = cv2.drawContours(tmp, [boxb[0]], 0, 128, thickness=cv2.FILLED)
                print("---")
                #

                # 占比判断(相似度，邻近度）
                areasize_a = boxa[4]
                areasize_b = boxb[4]
                areaplus = areasize_a + areasize_b
                areatotal = self.boxPointsArea(bbox)
    
                # Debug
                print("arearatio: " + str(areaplus/areatotal))
                #

                # 大小差异过于悬殊
                sizeratio = areasize_a/areasize_b
                if sizeratio < 1.0:
                    sizeratio = 1.0 / sizeratio

                if sizeratio > 10:
                    lines_img = cv2.drawContours(lines_img, [np.int0(boxa[0])], 0, 255, thickness=cv2.FILLED)
                    lines_img = cv2.drawContours(lines_img, [np.int0(boxb[0])], 0, 255, thickness=cv2.FILLED)
                    continue
                 
                # 非常接近，直接合并
                if areaplus/areatotal > 0.90:
                    lines_img = cv2.drawContours(lines_img, [np.int0(bbox)], 0, 255, thickness=cv2.FILLED)
                    retflag = True
                    continue
                
                # checkarearatio = 0.65
                # checkarearatio = -0.00247*(sizeratio-10)*(sizeratio-10)+0.80
                # checkarearatio = 0.0278*sizeratio+0.6222
                checkarearatio = self.getCheckAreaRatio(areasize_a, areasize_b)

                # Debug
                print("sizeratio : " + str(sizeratio) +"(" + str(areasize_a) +","+str(areasize_b) +")")
                print("checkarearatio: " + str(checkarearatio))
                #

                if areaplus/areatotal > checkarearatio:

                    # 横纵比判断
                    aspectratio_a = boxa[6]
                    aspectratio_b = boxb[6]

                    # Debug
                    print("aspectratio: " + str(aspectratio_a) + " " + str(aspectratio_b))
                    #

                    if aspectratio_a < 1.5 or aspectratio_b < 1.5:

                        # 方向平行或垂直
                        direction_a = boxa[5]
                        direction_b = boxb[5]
                        direction_2boxes = self.getDirectionFor2Box(boxa[0], boxb[0])
                        delta_direction = abs(direction_a-direction_b)
                        if delta_direction > math.pi/2:
                            delta_direction = math.pi - delta_direction

                        # Debug
                        print("Direction1: " + str(delta_direction))
                        #

                        # 判断两个BOX的方向
                        if delta_direction < math.pi/180*10 or delta_direction > math.pi/180*80:
                            delta_direction = abs(direction_a - direction_2boxes)
                            if delta_direction > math.pi/2:
                                delta_direction = math.pi - delta_direction

                            # Debug
                            print("Direction2: " + str(delta_direction))
                            #

                            # 判断BOX与两个BOX中心点连线方向
                            if delta_direction < math.pi/180*10 or delta_direction > math.pi/180*80:
                                # 是平行或垂直方向
                                lines_img = cv2.drawContours(lines_img, [np.int0(bbox)], 0, 255, thickness=cv2.FILLED)
                                retflag = True
                            else:
                                lines_img = cv2.drawContours(lines_img, [np.int0(boxa[0])], 0, 255, thickness=cv2.FILLED)
                                lines_img = cv2.drawContours(lines_img, [np.int0(boxb[0])], 0, 255, thickness=cv2.FILLED)
                        else:
                            lines_img = cv2.drawContours(lines_img, [np.int0(boxa[0])], 0, 255, thickness=cv2.FILLED)
                            lines_img = cv2.drawContours(lines_img, [np.int0(boxb[0])], 0, 255, thickness=cv2.FILLED)
                    else:
                    # 只能平行方向

                        # 方向平行
                        direction_a = boxa[5]
                        direction_b = boxb[5]
                        direction_2boxes = self.getDirectionFor2Box(boxa[0], boxb[0])
                        delta_direction = abs(direction_a-direction_b)
                        if delta_direction > math.pi/2:
                            delta_direction = math.pi - delta_direction

                        # Debug
                        print("Direction1: " + str(delta_direction))
                        #

                        # 判断两个BOX的方向
                        if delta_direction < math.pi/180*10:
                            delta_direction = abs(direction_a - direction_2boxes)
                            if delta_direction > math.pi/2:
                                delta_direction = math.pi - delta_direction
                            # 判断BOX与两个BOX中心点连线方向

                            # Debug
                            print("Direction2: " + str(delta_direction))
                            #

                            if delta_direction < math.pi/180*10:
                                # 是平行或垂直方向
                                lines_img = cv2.drawContours(lines_img, [np.int0(bbox)], 0, 255, thickness=cv2.FILLED)
                                retflag = True
                            else:
                                lines_img = cv2.drawContours(lines_img, [np.int0(boxa[0])], 0, 255, thickness=cv2.FILLED)
                                lines_img = cv2.drawContours(lines_img, [np.int0(boxb[0])], 0, 255, thickness=cv2.FILLED)
                        else:
                            lines_img = cv2.drawContours(lines_img, [np.int0(boxa[0])], 0, 255, thickness=cv2.FILLED)
                            lines_img = cv2.drawContours(lines_img, [np.int0(boxb[0])], 0, 255, thickness=cv2.FILLED)
                else:
                    lines_img = cv2.drawContours(lines_img, [np.int0(boxa[0])], 0, 255, thickness=cv2.FILLED)
                    lines_img = cv2.drawContours(lines_img, [np.int0(boxb[0])], 0, 255, thickness=cv2.FILLED)
                

        self.binaries = lines_img
        return len(contours)

        # plt.subplot(121)
        # plt.imshow(self.binaries)
        # plt.subplot(122)
        # plt.imshow(lines_img)
        # plt.show()

    def delsmallregions(self):
        boxes = []
        img = np.zeros_like(self.binaries)
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i, ctr in enumerate(contours):
            ro_rect = cv2.minAreaRect(ctr)
            box = np.int0(cv2.boxPoints(ro_rect))
            if self.boxPointsArea(box) > 300:
                img = cv2.drawContours(img, [np.int0(box)], 0, 255, thickness=cv2.FILLED)
        self.binaries = img
    

    def boxPointsArea(self, box):
        p0=np.array(box[0])
        p1=np.array(box[1])
        p2=np.array(box[2])
        l1=p1-p0
        l2=p1-p2
        d1=math.hypot(l1[0],l1[1])
        d2=math.hypot(l2[0],l2[1])
        return d1*d2
 
    def boxDirection(self, upleft, upright, downleft):
        h = upright - upleft
        v = downleft - upleft
        dh=math.hypot(h[0],h[1])
        dv=math.hypot(v[0],v[1])

        if dh > dv:
            d = h*[1,-1]
        else: 
            d = v*[1,-1]
        return math.asin(d[1]/math.hypot(d[0],d[1]))

    def boxAspectRatio(self, upleft, upright, downleft):
        h = upright - upleft
        v = downleft - upleft
        dh=math.hypot(h[0],h[1])
        dv=math.hypot(v[0],v[1])

        ratio = dh/dv
        if (ratio < 0):
            ratio = 1/ratio
        return ratio

    def getUpleftPnt(self, box):
        mostleft2x = np.sort(box[:,0])[0:2]
        mostup2y = np.sort(box[:,1])[0:2]
        for x in mostleft2x:
            for y in mostup2y:
                if self.isPointinBox(x, y, box):
                    return [x,y]

    def getUprightPnt(self, box):
        mostleft2x = np.sort(box[:,0])[-2:]
        mostup2y = np.sort(box[:,1])[0:2]
        for x in mostleft2x:
            for y in mostup2y:
                if self.isPointinBox(x, y, box):
                    return [x,y]

    def getDownleftPnt(self, box):
        mostleft2x = np.sort(box[:,0])[0:2]
        mostup2y = np.sort(box[:,1])[-2:]
        for x in mostleft2x:
            for y in mostup2y:
                if self.isPointinBox(x, y, box):
                    return [x,y]

    def isPointinBox(self, x, y, box):
        for i in range(0,4):
            if (x,y) == tuple(box[i]):
                return True
        return False

    def getDirectionFor2Box(self, boxa, boxb):
        minx2boxa = np.sort(boxa[:,0])[0]
        maxx2boxa = np.sort(boxa[:,0])[-1]
        miny2boxa = np.sort(boxa[:,1])[0]
        maxy2boxa = np.sort(boxa[:,1])[-1]
        centerx_boxa = (minx2boxa + maxx2boxa)/2
        centery_boxa = (miny2boxa + maxy2boxa)/2

        minx2boxb = np.sort(boxb[:,0])[0]
        maxx2boxb = np.sort(boxb[:,0])[-1]
        miny2boxb = np.sort(boxb[:,1])[0]
        maxy2boxb = np.sort(boxb[:,1])[-1]
        centerx_boxb = (minx2boxb + maxx2boxb)/2
        centery_boxb = (miny2boxb + maxy2boxb)/2

        direction = np.array([centerx_boxa, centery_boxa]) - np.array([centerx_boxb, centery_boxb])
        direction = direction*[1,-1]
        if direction[0] < 0:
            direction = direction*-1
        return math.asin(direction[1]/math.hypot(direction[0],direction[1]))

    def getCheckAreaRatio(self, areasize_a, areasize_b):

        sizeratio = areasize_a/areasize_b
        if sizeratio < 1.0:
            sizeratio = 1.0 / sizeratio

        if areasize_a < 200 or areasize_b < 200:
            if sizeratio < 5.0:
                return 0.5

        if areasize_a < 500 or areasize_b < 500:
            if sizeratio < 4.0:
                return 0.7

        if areasize_a < 800 or areasize_b < 800:
            if sizeratio < 2.0:
                return 0.725

        return 0.75










