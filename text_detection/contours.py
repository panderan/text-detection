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


## 计算 BOX 的面积大小
# 
def get_box_area(box):
    p0=np.array(box[0])
    p1=np.array(box[1])
    p2=np.array(box[2])
    l1=p1-p0
    l2=p1-p2
    d1=math.hypot(l1[0],l1[1])
    d2=math.hypot(l2[0],l2[1])
    return d1*d2


## 边界处理类
#
# 用于从二值图像中取得连通域边界
#
class tdcontours:
    
    ## 构造函数
    #
    # @param binaries 输入的二值图像
    # @param name 文件名
    # @param save_path 保存每个区域到文件的路径
    #
    def __init__(self, binaries=None, name="", save_path=""):
        self.binaries = binaries
        self.name = name
        self.boxes = []
        self.save_path = save_path
        self.t_of_fixed_area_ratio_for_rect = [0.99, 0.95, 0.90]
        self.t_of_extreme_area_ratio_for_ab = 24

    ## 将每一个候选区域存为图像文件
    # 将每一个候选区域交互保存为图像文件，并在过程中人为交互标记该候选区是否是文字区域
    #
    # @param orig_img 原图
    #
    # @retval retimg 在灰度图像中标记所有选区的图像
    #
    def save_each_contours(self, orig_img, save=True):
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        retimg = orig_img.copy()
        tmp = np.zeros_like(self.binaries)
        for i, (ctr, hiry) in enumerate(zip(contours, hierarchies[0])):
            if hiry[3] == -1:
                # 区域掩码图
                mask = np.zeros_like(self.binaries)
                mask = cv2.drawContours(mask, [ctr], 0, 255, thickness=cv2.FILLED)
                x,y,w,h = cv2.boundingRect(ctr)
                mask_seg = mask[y:y+h, x:x+w]
                 
                # 区域灰度图
                gray_img = np.zeros_like(self.binaries)
                gray_img[mask > 0] = orig_img[mask > 0]
                gray_img_seg = gray_img[ y:y+h, x:x+w]
                
                # 绘制图像
                ro_rect = cv2.minAreaRect(ctr)
                box = cv2.boxPoints(ro_rect)
                box = np.int0(box)
                bx,by,bw,bh = cv2.boundingRect(box)
                gray_img_copy = cv2.drawContours(gray_img.copy(), [box], 0, 255)
                retimg = cv2.drawContours(retimg, [box], 0, 255)
                
                # 标记并保存图像
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

    ## 文本块提取
    #
    # 将分散的连通域进行合并
    #
    def aggreate_contours_using_boxes(self, debug=False):
        # 提取掩码图中每个连通区域的最小外接矩形 Boxes
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i, ctr in enumerate(contours):
            ro_rect = cv2.minAreaRect(ctr)
            box = np.int0(cv2.boxPoints(ro_rect))
            self.boxes.append(np.int0(box))
        self._generate_binaries_using_boxes()
        
        # 进行 Boxes 的迭代合并
        num1 = self._aggreate_contours_using_boxes_once(debug=debug)
        self._generate_binaries_using_boxes()
        numx = self._aggreate_contours_using_boxes_once(debug=debug)
        self._generate_binaries_using_boxes()
        while (numx != num1):
            num1 = numx
            numx = self._aggreate_contours_using_boxes_once(debug=debug)
            self._generate_binaries_using_boxes()
        self._delsmallregions_using_boxes()

        # 生成最终掩码图
        self._generate_binaries_using_boxes()

    ## 连通域合并
    #
    # 合并两个连通域
    #
    def _aggreate_contours_using_boxes_once(self, debug=False):
        # 初始化每一个 Box，并计算每一个 Box 的相关参数
        boxes = []
        for i, box  in enumerate(self.boxes):
            downleft = box[0]
            upleft = box[1] 
            upright = box[2] 
            areasize = self._get_box_area(box)
            direction = self._get_box_direction(np.array(upleft), np.array(upright), np.array(downleft))
            aspectratio = self._get_box_aspect_ratio(np.array(upleft), np.array(upright), np.array(downleft))
            boxes.append((box, upleft, upright, downleft, areasize, direction, aspectratio))
        
        # 两两循环判断
        for i,boxa in enumerate(boxes):
            agged_flag = False              # 记录是否有 Box 可以合并
            candidate_agged_boxes = []      # 记录可以合并的 Box
            for j,boxb in enumerate(boxes[i+1:]):
                bbox_points = np.int0(np.array(boxa[0].tolist()+boxb[0].tolist()))
                bbox = cv2.boxPoints(cv2.minAreaRect(bbox_points))
                
                # 相关数据获取
                area_size_a = boxa[4]                                           # boxa 的面积
                area_size_b = boxb[4]                                           # boxb 的面积
                area_plus_ab = area_size_a + area_size_b                        # boxa 加 boxb 的面积
                area_bounding_rect = self._get_box_area(bbox)                   # boxa 和 boxb 共同外接矩形的面积
                size_ratio_of_ab = self._let_num_gt_1(area_size_a/area_size_b)  # boxa 和 boxb 的面积比
                size_ratio_of_bounding_rect = area_plus_ab/area_bounding_rect   # boxa 和 boxb 的面积和与外接矩形的面积比
                aspect_ratio_a = boxa[6]                                        # boxa 的长宽比
                aspect_ratio_b = boxb[6]                                        # boxb 的长宽比
                direction_a = boxa[5]                                           # boxa 的方向
                direction_b = boxb[5]                                           # boxb 的方向 

                # Debug print
                print("======================================================")
                print("Box a:")
                print("  area size:     %.3f" % area_size_a)
                print("  aspect ratio:  %.3f" % aspect_ratio_a)
                print("  direction:     %.3f" % direction_a)
                print("Box b:")
                print("  area size:     %.3f" % area_size_b)
                print("  aspect ratio:  %.3f" % aspect_ratio_b)
                print("  direction:     %.3f" % direction_b)
                print("Compare")
                print("  size_a/size_b: %.3f" % size_ratio_of_ab)
                print("  plus/rect:     %.3f" % size_ratio_of_bounding_rect)

                # 接近重叠嵌套
                if area_plus_ab/area_bounding_rect > self.t_of_fixed_area_ratio_for_rect[0]:
                    retboxes = self._aggreate_contours_2boxes(self.boxes, i, i+j+1)
                    self.boxes = retboxes
                    print("Overlap.")
                    self._debug_judge_2boxes_show(boxa[0], boxb[0], True, debug)
                    return len(self.boxes)

                # 非常接近，直接合并
                if area_plus_ab/area_bounding_rect > self.t_of_fixed_area_ratio_for_rect[1]:
                    if self._judge_direction(boxa[0], boxb[0], aspect_ratio_a, aspect_ratio_b, direction_a, direction_b):
                        retboxes = self._aggreate_contours_2boxes(self.boxes, i, i+j+1)
                        self.boxes = retboxes
                        print("Very close.")
                        self._debug_judge_2boxes_show(boxa[0], boxb[0], True, debug)
                        return len(self.boxes)

                # 大小差异过于悬殊
                if size_ratio_of_ab > self.t_of_extreme_area_ratio_for_ab:
                    print("The difference is huge.")
                    self._debug_judge_2boxes_show(boxa[0], boxb[0], False, debug)
                    continue
                 
                # 非常接近，直接合并
                if area_plus_ab/area_bounding_rect > self.t_of_fixed_area_ratio_for_rect[2]:
                    if self._judge_direction(boxa[0], boxb[0], aspect_ratio_a, aspect_ratio_b, direction_a, direction_b):
                        candidate_agged_boxes.append((boxb[0], i+j+1, area_plus_ab/area_bounding_rect))
                        agged_flag = True
                        print("Very close (verify direction).")
                        self._debug_judge_2boxes_show(boxa[0], boxb[0], True, debug)
                        continue
                
                # 按两个 Box 的相关数据动态判断是否合并
                t_of_area_ratio_for_rect = self._get_threshold_of_area_ratio(area_size_a, area_size_b, aspect_ratio_a, aspect_ratio_b)
                print("  T of area ratio:   %.3f" % t_of_area_ratio_for_rect)
                if area_plus_ab/area_bounding_rect > t_of_area_ratio_for_rect:
                    if self._judge_direction(boxa[0], boxb[0], aspect_ratio_a, aspect_ratio_b, direction_a, direction_b):
                        candidate_agged_boxes.append((boxb[0], i+j+1, area_plus_ab/area_bounding_rect))
                        agged_flag = True
                        print("Pass validation")
                        self._debug_judge_2boxes_show(boxa[0], boxb[0], True, debug)
                    else:
                        print("Not pass validation (direction)")
                        self._debug_judge_2boxes_show(boxa[0], boxb[0], False, debug)
                        pass
                else:
                    print("Not pass validation (area_size_for_rect)")
                    self._debug_judge_2boxes_show(boxa[0], boxb[0], False, debug)
                    pass

            # 从符号合并的候选区域中找出最符合的一个进行合并
            if agged_flag == True:
                print("---------------- Aggregating ----------------")
                max_aggbox = candidate_agged_boxes[0]
                for idx,aggbox in enumerate(candidate_agged_boxes):
                    if max_aggbox[2] < aggbox[2]:
                        max_aggbox = aggbox
                retboxes = self._aggreate_contours_2boxes(self.boxes, i, max_aggbox[1])
                self.boxes = retboxes
                self._debug_aggreate_boxes_show(candidate_agged_boxes, boxa[0],max_aggbox[0], debug)
                return len(self.boxes)
            agged_flag = False
                
        return len(self.boxes)
    
    ## 对两个 Box 进行合并
    #
    # @param boxes 所有 Box 的列表
    # @param idxi Box1 的下标
    # @param idxj Box2 的小标
    #
    # @retval retboxes 合并好的所有 Box 列表
    #
    def _aggreate_contours_2boxes(self, boxes, idxi, idxj):
        retboxes = []
        for i,box in enumerate(boxes):
            if i != idxi and i !=idxj:
                retboxes.append(box)

        bbox_points = np.int0(np.array(boxes[idxi].tolist()+boxes[idxj].tolist()))
        bbox = cv2.boxPoints(cv2.minAreaRect(bbox_points))
        retboxes.append(bbox)
        return retboxes

    ## 按面积进行筛选，过滤掉面积过小的 Box
    #
    # @retval retboxes 筛选后的所有 Box 列表
    #
    def _delsmallregions_using_boxes(self):
        retboxes = []
        for i,box in enumerate(self.boxes):
            if self._get_box_area(box) > 140:
                retboxes.append(box)
        self.boxes = retboxes

    ## 使用 Boxes 重新生成掩码图
    # 
    # 这个过程会过滤掉较小的 Box，如 delsmallregions_using_boxes。
    #
    def _generate_binaries_using_boxes(self):
        binaries = np.zeros_like(self.binaries)
        new_boxes = []
        for i,box in enumerate(self.boxes):
            if self._get_box_area(box) > 140:
                binaries = cv2.drawContours(binaries, [np.int0(box)], 0, 255, thickness=cv2.FILLED)
                new_boxes.append(box)

        self.binaries = binaries
        self.boxes = new_boxes

    ## 计算 Box 的面积
    #
    # @return Box 的面积
    #
    def _get_box_area(self, box):
        p0=np.array(box[0])
        p1=np.array(box[1])
        p2=np.array(box[2])
        l1=p1-p0
        l2=p1-p2
        d1=math.hypot(l1[0],l1[1])
        d2=math.hypot(l2[0],l2[1])
        return d1*d2
 
    ## 计算 Box 的方向
    #
    # @return Box 的方向
    #
    def _get_box_direction(self, upleft, upright, downleft):
        h = upright - upleft
        v = downleft - upleft
        dh=math.hypot(h[0],h[1])
        dv=math.hypot(v[0],v[1])

        if dh > dv:
            d = h*[1,-1]
        else: 
            d = v*[1,-1]
        return math.asin(d[1]/math.hypot(d[0],d[1]))
    
    ## 获取 Box 的长宽比
    #
    # @return Box 的长宽比
    #
    def _get_box_aspect_ratio(self, upleft, upright, downleft):
        h = upright - upleft
        v = downleft - upleft
        dh=math.hypot(h[0],h[1])
        dv=math.hypot(v[0],v[1])

        ratio = dh/dv
        if (ratio < 1.0):
            ratio = 1.0/ratio
        return ratio
    
    ## 计算两个 Box 中心连线的方向
    #
    # @return 两个 Box 中心连线的方向
    #
    def _get_box_centers_direction(self, boxa, boxb):
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

    ## 依据两个 Box 的数据获取其位置比率阈值
    #
    # @param areasize_a Box1 的面积
    # @param areasize_b Box2 的面积
    # @param aspectratio_a Box1 的长宽比
    # @param aspectratio_b Box2 的长宽比
    #
    # @return 阈值
    #
    def _get_threshold_of_area_ratio(self, areasize_a, areasize_b, aspectratio_a, aspectratio_b):

        sizeratio = areasize_a/areasize_b
        if sizeratio < 1.0:
            sizeratio = 1.0 / sizeratio

        if areasize_a < 200 or areasize_b < 200:
            if sizeratio < 5.0:
                return 0.5

        if areasize_a < 600 or areasize_b < 600:
            if sizeratio < 2.0:
                return 0.53
            if sizeratio < 3.0:
                return 0.58
            if sizeratio < 3.5:
                return 0.63
            if sizeratio < 4.0:
                return 0.68

        if areasize_a < 800 or areasize_b < 800:
            if sizeratio < 2.0:
                retval = self._get_threshold_of_area_ratio_with_aspectratio(aspectratio_a, aspectratio_b)
                if retval < 0.1:
                    return 0.710
                else:
                    return retval

        if areasize_a < 1000 or areasize_b < 1000:
            if sizeratio < 2.0:
                retval = self._get_threshold_of_area_ratio_with_aspectratio(aspectratio_a, aspectratio_b)
                if retval < 0.1:
                    return 0.715
                else:
                    return retval
        
        retval = self._get_threshold_of_area_ratio_with_aspectratio(aspectratio_a, aspectratio_b)
        if retval < 0.1:
            retval = 0.72
        return retval

    def _get_threshold_of_area_ratio_with_aspectratio(self, aspectratio_a, aspectratio_b):
        rate = aspectratio_a/aspectratio_b
        if rate < 1.0:
            rate = 1.0/rate

        if aspectratio_a > 8.0 or aspectratio_b > 8.0:
            return 0.8 

        if aspectratio_a < 2.0 or aspectratio_b < 2.0:
            if rate < 1.2:
                return 0.66
            return 0.70

        if aspectratio_a < 1.25 or aspectratio_b < 1.25:
            if rate < 1.2:
                return 0.64
            return 0.68
        return 0


    ## 获取判断方向类别的阈值
    #
    # 低于阈值允许大致平行或垂直；高于阈值只允许平行
    #
    def _get_threshold_of_direction_type(self, boxa, boxb):
        areasize_a = self._get_box_area(boxa)
        areasize_b = self._get_box_area(boxb)
        if areasize_a < 200 or areasize_b < 200:
            return 4.0
        if areasize_a < 400 or areasize_b < 400:
            return 3.0    
        if areasize_a < 800 or areasize_b < 800:
            return 2.0
        return 1.5
    
    ## 获取判断方向的精度
    #
    # 默认方向夹角小于20度，则认为平行。大于70度认为垂直
    #
    def _get_threshold_of_angle_precision(self, boxa, boxb, aspectratio_a, aspectratio_b):
        areasize_a = self._get_box_area(boxa)
        areasize_b = self._get_box_area(boxb)

        if aspectratio_a < 2.0 or aspectratio_b < 2.0:
            if areasize_a < 800 or areasize_b < 800:
                # 候选区域较小，忽略方向判断
                return math.pi/180*46
            else:
                return math.pi/180*35
        return math.pi/180*20

    ## 对两个 Box 的方向进行可合并判别
    #
    def _judge_direction(self, boxa, boxb, aspectratio_a, aspectratio_b, direction_a, direction_b):

        # 两个 BOX 中心点连线的方向
        direction_2boxes = self._get_box_centers_direction(boxa, boxb)
        
        # 两个 BOX 方向的差
        delta_direction_2boxes = abs(direction_a-direction_b)
        if delta_direction_2boxes > math.pi/2:
            delta_direction_2boxes = math.pi - delta_direction_2boxes
        
        # 其中一个 BOX 与中心点连线方向的差
        delta_direction_box_with_centers = abs(direction_a - direction_2boxes)
        if delta_direction_box_with_centers > math.pi/2:
            delta_direction_box_with_centers = math.pi - delta_direction_box_with_centers

        min_threshold = self._get_threshold_of_angle_precision(boxa, boxb, aspectratio_a, aspectratio_b)
        max_threshold = math.pi/2 - min_threshold

        aspectratio_threshod = self._get_threshold_of_direction_type(boxa, boxb)

        # Debug output
        print("  direction 2-boxes:       %.3f" % delta_direction_2boxes)
        print("  direction centers:       %.3f" % delta_direction_box_with_centers)
        print("  T of direction type:     %.3f" % aspectratio_threshod)
        print("  precision of direction: (%.3f,%.3f)" % (min_threshold, max_threshold))

        if aspectratio_a < aspectratio_threshod or aspectratio_b < aspectratio_threshod:
        # 方向平行或垂直
            # 判断两个BOX的方向
            if delta_direction_2boxes < min_threshold or delta_direction_2boxes > max_threshold:

                # 判断BOX与两个BOX中心点连线方向
                if delta_direction_box_with_centers < min_threshold or delta_direction_box_with_centers > max_threshold:
                    return True
                else:
                    return False
            else:
                return False
        else:
        # 只能平行方向
            # 判断两个BOX的方向
            if delta_direction_2boxes < min_threshold:

                # 判断BOX与两个BOX中心点连线方向
                if delta_direction_box_with_centers < max_threshold:
                    return True
                else:
                    return False
            else:
                return False

    def _let_num_gt_1(self, num):
        if num < 1.0:
            return 1.0 / num
        return num

    @property
    def binaries(self):
        return self.__binaries
    @binaries.setter
    def binaries(self, val):
        self.__binaries = val

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, val):
        self.__name = val

    @property
    def boxes(self):
        return self.__boxes
    @boxes.setter
    def boxes(self, val):
        self.__boxes = val

    @property
    def save_path(self):
        return self.__save_path
    @save_path.setter
    def save_path(self, val):
        self.__save_path = val 
        if len(self.__save_path) > 0:
            if self.__save_path[-1] != '/':
                self.__save_path += '/'

    @property
    def t_of_fixed_area_ratio_for_rect(self):
        return self.__t_of_fixed_area_ratio_for_rect
    @t_of_fixed_area_ratio_for_rect.setter
    def t_of_fixed_area_ratio_for_rect(self, val):
        self.__t_of_fixed_area_ratio_for_rect = val

    @property
    def t_of_extreme_area_ratio_for_ab(self):
        return self.__t_of_extreme_area_ratio_for_ab
    @t_of_extreme_area_ratio_for_ab.setter
    def t_of_extreme_area_ratio_for_ab(self, val):
        self.__t_of_extreme_area_ratio_for_ab = val

    def _debug_judge_2boxes_show(self, boxa, boxb, flag, is_enable=False):
        if flag:
            print("True")
        else:
            print("False")

        if is_enable == True:
            tmp = self.binaries.copy()
            tmp = cv2.drawContours(tmp, [np.int0(boxa)], 0, 85, thickness=cv2.FILLED)
            tmp = cv2.drawContours(tmp, [np.int0(boxb)], 0, 170, thickness=cv2.FILLED)
            cv2.namedWindow("Debug",0);
            cv2.resizeWindow("Debug", 800, 600);
            cv2.imshow("Debug", tmp)
            cv2.waitKey(0)

    def _debug_aggreate_boxes_show(self, candidate_agged_boxes, added_box1, added_box2, is_enable=False):
        if is_enable == True:
            tmp = self.binaries.copy()
            for box in candidate_agged_boxes:
                tmp = cv2.drawContours(tmp, [np.int0(box[0])], 0, 170, thickness=cv2.FILLED)
            tmp = cv2.drawContours(tmp, [np.int0(added_box1)], 0, 90, thickness=cv2.FILLED)
            tmp = cv2.drawContours(tmp, [np.int0(added_box2)], 0, 90, thickness=cv2.FILLED)
            cv2.namedWindow("Debug",0);
            cv2.resizeWindow("Debug", 800, 600);
            cv2.imshow("Debug", tmp)
            cv2.waitKey(0)









