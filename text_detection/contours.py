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

PAR_BOX=0
PAR_UP_LEFT=1
PAR_UP_RIGHT=2
PAR_DOWN_LEFT=3
PAR_AREA_SIZE=4
PAR_DIRECTION=5
PAR_ASPECT_RATIO=6

DIRECTION_TYPE_NONE=1
DIRECTION_TYPE_PARALLEL=2
DIRECTION_TYPE_PARALLEL_CENTER_LINE=4
DIRECTION_TYPE_VERTICAL_ALLOWED=5

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
        self.t_of_extreme_area_ratio_for_ab = 24
        self.t_of_overlap_ratio = 0.25
        self.strategy = "Horizon"
        self.t_of_area_size = 140
        self.t_of_ar_of_direction_type = 2.5
        self.t_of_distance = 2.6

    ## 将每一个候选区域存为图像文件
    # 将每一个候选区域交互保存为图像文件，并在过程中人为交互标记该候选区是否是文字区域
    #
    # @param orig_img 原图
    #
    def save_each_contours_using_boxes(self, orig_img, save=True):
        for i, box in enumerate(self.boxes):
            # 区域掩码图
            box = np.int0(box)
            mask = np.zeros_like(self.binaries)
            mask = cv2.drawContours(mask, [box], 0, 255, thickness=cv2.FILLED)
            x,y,w,h = cv2.boundingRect(box)
            mask_seg = mask[y:y+h, x:x+w]
                 
            # 区域灰度图
            gray_img = np.zeros_like(self.binaries)
            gray_img[mask > 0] = orig_img[mask > 0]
            gray_img_seg = gray_img[ y:y+h, x:x+w]
                
            # 标记并保存图像
            if save==True:
                plt.ion()
                plt.imshow(gray_img_seg, "gray")
                plt.pause(0.2)
                judge = input("is text region? : ")
                if (judge == 'Y'):
                    cv2.imwrite(self.save_path + self.name+"-"+str(i)+"-Y.jpg", gray_img_seg)
                    cv2.imwrite(self.save_path + "mask/"+self.name+"-"+str(i)+"-Y-mask.jpg", mask_seg)
                else:
                    cv2.imwrite(self.save_path + self.name+"-"+str(i)+"-N.jpg", gray_img_seg)
                    cv2.imwrite(self.save_path + "mask/"+self.name+"-"+str(i)+"-N-mask.jpg", mask_seg)

    ## 文本块提取
    #
    # 将分散的连通域进行合并
    #
    def aggreate_contours_using_boxes(self, debug=False, debug_verbose=False):
        # 提取掩码图中每个连通区域的最小外接矩形 Boxes
        image, contours, hierarchies = cv2.findContours(self.binaries, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i, ctr in enumerate(contours):
            ro_rect = cv2.minAreaRect(ctr)
            box = np.int0(cv2.boxPoints(ro_rect))
            self.boxes.append(np.int0(box))
        self._generate_binaries_using_boxes()
        
        # 进行 Boxes 的迭代合并
        num1 = self._aggreate_contours_using_boxes_once(debug=debug, debug_verbose=debug_verbose)
        self._generate_binaries_using_boxes()
        numx = self._aggreate_contours_using_boxes_once(debug=debug, debug_verbose=debug_verbose)
        self._generate_binaries_using_boxes()
        while (numx != num1):
            num1 = numx
            numx = self._aggreate_contours_using_boxes_once(debug=debug, debug_verbose=debug_verbose)
            self._generate_binaries_using_boxes()
        self._delsmallregions_using_boxes()

        # 生成最终掩码图
        self._generate_binaries_using_boxes()

    ## 连通域合并
    #
    # 合并两个连通域
    #
    def _aggreate_contours_using_boxes_once(self, debug=False, debug_verbose=False):
        # 初始化每一个 Box，并计算每一个 Box 的相关参数
        boxes = []
        for i, box  in enumerate(self.boxes):
            downleft = box[0]
            upleft = box[1] 
            upright = box[2] 
            areasize,_,_ = self._get_box_area(box)
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
                area_bounding_rect,_,_ = self._get_box_area(bbox)               # boxa 和 boxb 共同外接矩形的面积
                size_ratio_of_ab = self._let_num_gt_1(area_size_a/area_size_b)  # boxa 和 boxb 的面积比
                size_ratio_of_bounding_rect = self._get_pos_ratio(boxa, boxb)   # boxa 和 boxb 的面积和与外接矩形的面积比
                aspect_ratio_a = boxa[6]                                        # boxa 的长宽比
                aspect_ratio_b = boxb[6]                                        # boxb 的长宽比
                direction_a = boxa[5]                                           # boxa 的方向
                direction_b = boxb[5]                                           # boxb 的方向 
                overlap_ratio = self._get_overlap_ratio(boxa, boxb)
                area_size_a_tmp,w_a_tmp,h_a_tmp = self._get_box_area(boxa[0])
                area_size_b_tmp,w_b_tmp,h_b_tmp = self._get_box_area(boxb[0])

                # Debug print
                if debug:
                    print("======================================================")
                    print("Box a:")
                    print("  area size:     %.3f(%.3f,%.3f,%.3f)" % (area_size_a, area_size_a_tmp, w_a_tmp, h_a_tmp))
                    print("  aspect ratio:  %.3f" % aspect_ratio_a)
                    print("  direction:     %.3f" % direction_a)
                    print("Box b:")
                    print("  area size:     %.3f(%.3f,%.3f,%.3f)" % (area_size_b, area_size_b_tmp, w_b_tmp, h_b_tmp))
                    print("  aspect ratio:  %.3f" % aspect_ratio_b)
                    print("  direction:     %.3f" % direction_b)
                    print("Compare")
                    print("  overlap ratio: %.3f" % overlap_ratio)
                    print("  size_a/size_b: %.3f" % size_ratio_of_ab)

                # 重叠嵌套判别
                if overlap_ratio > self.t_of_overlap_ratio:
                    retboxes = self._aggreate_contours_2boxes(self.boxes, i, i+j+1)
                    self.boxes = retboxes
                    if debug:
                        print("Overlap. \n%s" % True)
                        self._debug_judge_2boxes_show(boxa[0], boxb[0], debug_verbose)
                    return len(self.boxes)

                # 按两个 Box 的相关数据动态判断是否合并
                t_of_area_ratio_for_rect = self._get_threshold_of_area_ratio(boxa, boxb)
                if debug:
                    print("  plus/rect:     %.3f(%.3f)" % (size_ratio_of_bounding_rect, t_of_area_ratio_for_rect))
                if size_ratio_of_bounding_rect > t_of_area_ratio_for_rect:
                    if self._judge_direction(boxa, boxb, debug) and self._judge_distance(boxa, boxb, debug) and self._judge_strategy(boxa, boxb, debug):
                        candidate_agged_boxes.append((boxb[0], i+j+1, area_plus_ab/area_bounding_rect))
                        agged_flag = True
                        if debug:
                            print("Pass validation \n%s" % True)
                            self._debug_judge_2boxes_show(boxa[0], boxb[0], debug_verbose)
                    else:
                        if debug:
                            print("Not pass validation (direction or distance) \n%s" % False)
                            self._debug_judge_2boxes_show(boxa[0], boxb[0], debug_verbose)
                else:
                    if debug:
                        print("Not pass validation (pos_size_for_rect) \n%s" % False)
                        self._debug_judge_2boxes_show(boxa[0], boxb[0], debug_verbose)


            # 从符号合并的候选区域中找出最符合的一个进行合并
            if agged_flag == True:
                agg_idx = self._pickup_best_agg_box(boxa, candidate_agged_boxes)
                retboxes = self._aggreate_contours_2boxes(self.boxes, i, agg_idx)
                if debug:
                    print("---------------- Aggregating ----------------")
                    self._debug_aggreate_boxes_show(candidate_agged_boxes, boxa[0], self.boxes[agg_idx], debug)
                self.boxes = retboxes
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
        retboxes.insert(0,bbox)
        return retboxes
    
    def _pickup_best_agg_box(self, boxa, agg_boxes):
        if len(agg_boxes) == 1:
            return agg_boxes[0][1]
        
        best_box = agg_boxes[0]
        center_point_a = self._get_box_center_point(boxa[PAR_BOX])
        center_point_tmp = self._get_box_center_point(best_box[0])
        best_val = -1.0

        for candidate_box in agg_boxes:
            if self.strategy == "Horizon":
                center_point_tmp = self._get_box_center_point(candidate_box[0])
                if best_val < 0.0 or best_val < abs(center_point_a[0]-center_point_tmp[0]):
                    best_box = candidate_box
                    best_val = abs(center_point_a[0]-center_point_tmp[0])
            elif self.strategy == "Vertical":
                center_point_tmp = self._get_box_center_point(candidate_box[0])
                if best_val < 0.0 or best_val < abs(center_point_a[1]-center_point_tmp[1]):
                    best_box = candidate_box
                    best_val = abs(center_point_a[1]-center_point_tmp[1])
            else:
                if best_val > candidate_box[2]:
                    best_box = candidate_box
                    best_val = candidate_box[2]

        return best_box[1]        


    ## 按面积进行筛选，过滤掉面积过小的 Box
    #
    # @retval retboxes 筛选后的所有 Box 列表
    #
    def _delsmallregions_using_boxes(self):
        retboxes = []
        for i,box in enumerate(self.boxes):
            area_size,_,_ = self._get_box_area(box)
            if area_size > 140:
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
            points = [x for y in box for x in y]
            points.sort()
            if points[0] < 0:
                continue
            area_size,_,_ = self._get_box_area(box)
            if area_size > self.t_of_area_size:
                binaries = cv2.drawContours(binaries, [np.int0(box)], 0, 255, thickness=cv2.FILLED)
                new_boxes.append(np.int0(box))

        self.binaries = binaries
        self.boxes = new_boxes
    
    def flesh_binaries_using_boxes(self):
        self._generate_binaries_using_boxes()

    def flesh_binaries_using_filtered_boxes(self, flt):
        new_boxes = []
        for box in self.boxes:
            if type(flt) != type(None) and flt.verification(box) == False:
                continue
            new_boxes.append(np.int0(box))
        self.boxes = new_boxes
        self._generate_binaries_using_boxes()

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
        return (d1*d2, d1, d2)
 
    def _get_pos_ratio(self, boxa, boxb):
        area_size_a = boxa[4]
        area_size_b = boxb[4]
        area_plus_ab = area_size_a + area_size_b

        bbox_points = np.int0(np.array(boxa[0].tolist()+boxb[0].tolist()))
        bbox = cv2.boxPoints(cv2.minAreaRect(bbox_points))
        area_bounding_rect,_,_ = self._get_box_area(bbox)
        size_ratio_of_bounding_rect = area_plus_ab/area_bounding_rect

        return size_ratio_of_bounding_rect

    ## 计算重叠部分占较小 Box 的比率
    #
    def _get_overlap_ratio(self, boxa, boxb):
        mask_a = np.zeros_like(self.binaries)
        mask_b = np.zeros_like(self.binaries)

        min_size = boxa[PAR_AREA_SIZE]
        if boxa[PAR_AREA_SIZE] > boxb[PAR_AREA_SIZE]:
            min_size = boxb[PAR_AREA_SIZE]

        mask_a = cv2.drawContours(mask_a, [np.int0(boxa[PAR_BOX])], 0, 255, cv2.FILLED)
        mask_b = cv2.drawContours(mask_b, [np.int0(boxb[PAR_BOX])], 0, 255, cv2.FILLED)
        
        return (np.sum(mask_a & mask_b)/255.0)/min_size

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
    def _get_box_centers_direction(self, box1, box2):
        direction = np.array(self._get_box_center_point(box1)) \
                    - np.array(self._get_box_center_point(box2))
        direction = direction*[1,-1]
        if direction[0] < 0:
            direction = direction*-1
        return math.asin(direction[1]/math.hypot(direction[0],direction[1]))

    def _get_box_center_point(self, box):
        minx2box = np.sort(box[:,0])[0]
        maxx2box = np.sort(box[:,0])[-1]
        miny2box = np.sort(box[:,1])[0]
        maxy2box = np.sort(box[:,1])[-1]
        centerx_box = (minx2box + maxx2box)/2
        centery_box = (miny2box + maxy2box)/2
        return [centerx_box,centery_box]

    ## 依据两个 Box 的数据获取其位置比率阈值
    #
    # @param areasize_a Box1 的面积
    # @param areasize_b Box2 的面积
    # @param aspectratio_a Box1 的长宽比
    # @param aspectratio_b Box2 的长宽比
    #
    # @return 阈值
    #
    def _get_threshold_of_area_ratio(self, boxa, boxb):
        
        if self._is_gt_one_char(boxa[PAR_BOX]) == False:
            if boxa[PAR_ASPECT_RATIO] > 2.0:
                return 0.55
            else:
                return 0.60

        if self._is_gt_one_char(boxb[PAR_BOX]) == False:
            if boxb[PAR_ASPECT_RATIO] > 2.0:
                return 0.55
            else:
                return 0.60
        
        if boxa[PAR_ASPECT_RATIO] > 3.0 or boxb[PAR_ASPECT_RATIO] > 3.0:
            return 0.72
        elif boxa[PAR_ASPECT_RATIO] > 5.0 or boxb[PAR_ASPECT_RATIO] > 5.0:
            return 0.76
        elif boxa[PAR_ASPECT_RATIO] > 8.0 or boxb[PAR_ASPECT_RATIO] > 8.0:
            return 0.80
        else:
            return 0.70

    ## 获取判断方向类别的阈值
    #
    # 低于阈值允许大致平行或垂直；高于阈值只允许平行
    #
    def _get_threshold_of_direction_type(self, boxa, boxb):
        if self._is_gt_one_char(boxa[PAR_BOX]) or self._is_gt_one_char(boxb[PAR_BOX]):
            return False
        else:
            return True
    
    ## 获取判断方向的精度
    #
    # 默认方向夹角小于20度，则认为平行。大于70度认为垂直t_of_ar_of_direction_type
    #
    def _get_threshold_of_angle_precision(self, boxa, boxb=None):
        if (boxa != None and boxa[PAR_ASPECT_RATIO] < 2.0) \
             or (boxb != None and boxb[PAR_ASPECT_RATIO] < 2.0):
                return math.pi/180*35
        return math.pi/180*20

    ## 对两个 Box 的方向进行可合并判别
    #
    def _judge_direction(self, boxa, boxb, debug=False):
        if self._is_gt_one_char(boxa[PAR_BOX]) == False \
            and self._is_gt_one_char(boxb[PAR_BOX]) == False:
            return True
        
        # 获取方向判断类别 
        direction_type = DIRECTION_TYPE_PARALLEL
        if self._is_gt_one_char(boxa[PAR_BOX]) == False \
            or self._is_gt_one_char(boxb[PAR_BOX]) == False:
                direction_type = DIRECTION_TYPE_PARALLEL_CENTER_LINE

        if boxa[PAR_ASPECT_RATIO] < 1.5 or boxb[PAR_ASPECT_RATIO] < 1.5:
            direction_type |= DIRECTION_TYPE_VERTICAL_ALLOWED

        # 两个 BOX 方向的差 和
        # 其中一个面积较大的 BOX 与中心点连线方向的差
        delta_direction_2boxes = abs(boxa[PAR_DIRECTION]-boxb[PAR_DIRECTION]) % (math.pi/2)
        max_box = boxa[PAR_AREA_SIZE] > boxb[PAR_AREA_SIZE] and boxa or boxb
        direction_2boxes = self._get_box_centers_direction(boxa[PAR_BOX], boxb[PAR_BOX])
        delta_direction_box_with_centers = abs(max_box[PAR_DIRECTION] - direction_2boxes) % (math.pi/2)
        
        if direction_type == DIRECTION_TYPE_PARALLEL_CENTER_LINE:
            min_threshold = self._get_threshold_of_angle_precision(max_box)
        else:
            min_threshold = self._get_threshold_of_angle_precision(boxa, boxb)
        max_threshold = math.pi/2 - min_threshold

        # Debug output
        if debug:
            print("  direction 2-boxes:       %.3f" % delta_direction_2boxes)
            print("  direction centers:       %.3f" % delta_direction_box_with_centers)
            print("  precision of direction: (%.3f,%.3f)" % (min_threshold, max_threshold))
            print("  direction type:          %.3f" % direction_type)
            print("  is gt one char:          %s,%s" %  (self._is_gt_one_char(boxa[PAR_BOX]), self._is_gt_one_char(boxb[PAR_BOX])))

        if direction_type & DIRECTION_TYPE_PARALLEL:
            if delta_direction_2boxes < min_threshold \
                or (direction_type & DIRECTION_TYPE_VERTICAL_ALLOWED \
                    and delta_direction_2boxes > max_threshold):
                pass
            else:
                return False

        if direction_type & DIRECTION_TYPE_PARALLEL \
            or direction_type & DIRECTION_TYPE_PARALLEL_CENTER_LINE:
            if delta_direction_box_with_centers < min_threshold \
                or (direction_type & DIRECTION_TYPE_VERTICAL_ALLOWED \
                    and delta_direction_box_with_centers > max_threshold):
                pass
            else:
                return False

        return True


    def _judge_distance(self, boxa, boxb, debug=False):
        center_point_a = self._get_box_center_point(boxa[PAR_BOX])
        center_point_b = self._get_box_center_point(boxb[PAR_BOX])
        binaries_a = np.zeros_like(self.binaries)
        binaries_b = np.zeros_like(self.binaries)
        binaries_a = cv2.drawContours(binaries_a, [np.int0(boxa[0])], 0, 255, cv2.FILLED)
        binaries_b = cv2.drawContours(binaries_b, [np.int0(boxb[0])], 0, 255, cv2.FILLED)
        binaries_boxes = binaries_a|binaries_b
        binaries_line = binaries_boxes.copy()
        binaries_line = cv2.line(binaries_line, tuple(np.int0(center_point_a)), tuple(np.int0(center_point_b)), 255, thickness=1)
        binaries_ret = np.bitwise_xor(np.int0(binaries_boxes), np.int0(binaries_line))
        distance = np.sum(binaries_ret)/255.0

        area_size_a, w_a, h_a = self._get_box_area(boxa[PAR_BOX])
        area_size_b, w_b, h_b = self._get_box_area(boxb[PAR_BOX])
        min_area_size = area_size_a
        if min_area_size > area_size_b:
            min_area_size = area_size_b
        
        if debug:
            print("  distance 2-boxes:  %.3f(%.3f)" % (distance, self.t_of_distance * math.sqrt(min_area_size)))

        if distance < self.t_of_distance * math.sqrt(min_area_size):
            return True
        else:
            return False

    def _judge_strategy(self, boxa, boxb, debug):

        if self._is_gt_one_char(boxa[PAR_BOX]) == True and self._is_gt_one_char(boxb[PAR_BOX]) == True:
            return True
        
        big_box = boxa
        small_box = boxb 
        boxa_bounding_rect = cv2.boundingRect(boxa[PAR_BOX])    
        boxb_bounding_rect = cv2.boundingRect(boxb[PAR_BOX])
        big_box_bounding_rect = boxa_bounding_rect
        if boxa_bounding_rect[2]*boxa_bounding_rect[3] < boxb_bounding_rect[2]*boxb_bounding_rect[3]:
            big_box = boxb
            small_box = boxa
            big_box_bounding_rect = boxb_bounding_rect

        center_small = self._get_box_center_point(small_box[PAR_BOX])
        center_big = self._get_box_center_point(big_box[PAR_BOX])

        if self.strategy == "Horizon":
            if abs(center_small[0] - center_big[0]) > big_box_bounding_rect[2]/2.0:
                return True
            else:
                return False
        elif self.strategy == "Vertical":
            if abs(center_small[1] - center_big[1]) > big_box_bounding_rect[3]/2.0:
                return True
            else:
                return False
        else:
            return True


        area_size_a, w_a, h_a = self._get_box_area(boxa[PAR_BOX])
        area_size_b, w_b, h_b = self._get_box_area(boxb[PAR_BOX])
        center_point_a = self._get_box_center_point(boxa[PAR_BOX])
        center_point_b = self._get_box_center_point(boxb[PAR_BOX])
        max_area_size = area_size_a
        if max_area_size < area_size_b:
            max_area_size = area_size_b
        delta = 0.5*math.sqrt(max_area_size)

        if self.strategy == "Horizon":
            if abs(center_point_a[0] - center_point_b[0]) > delta:
                return True
            else:
                return False
        elif self.strategy == "Vertical":
            if abs(center_point_a[1] - center_point_b[1]) > delta:
                return True
            else:
                return False
        else:
            return True


       
    def _is_gt_one_char(self, box):
        area_size,w,h = self._get_box_area(box)
        if area_size > 1500:
            return True 
        if w > 60 or h > 60:
            return True 
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
    def t_of_extreme_area_ratio_for_ab(self):
        return self.__t_of_extreme_area_ratio_for_ab
    @t_of_extreme_area_ratio_for_ab.setter
    def t_of_extreme_area_ratio_for_ab(self, val):
        self.__t_of_extreme_area_ratio_for_ab = val

    @property
    def t_of_overlap_ratio(self):
        return self.__t_of_overlap_ratio
    @t_of_overlap_ratio.setter
    def t_of_overlap_ratio(self, val):
        self.__t_of_overlap_ratio = val

    @property
    def t_of_area_size(self):
        return self.__t_of_area_size
    @t_of_area_size.setter
    def t_of_area_size(self, val):
        self.__t_of_area_size = val

    @property
    def t_of_ar_of_direction_type(self):
        return self.__t_of_ar_of_direction_type
    @t_of_ar_of_direction_type.setter
    def t_of_ar_of_direction_type(self, val):
        self.__t_of_ar_of_direction_type = val

    @property
    def t_of_distance(self):
        return self.__t_of_distance
    @t_of_distance.setter
    def t_of_distance(self, val):
        self.__t_of_distance = val

    def _debug_judge_2boxes_show(self, boxa, boxb, is_enable=False):
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



class contours_car_license(tdcontours):
    def __init__(self, binaries=None, name="", save_path=""):
        super(contours_car_license, self).__init__(binaries, name, save_path)

    def _get_threshold_of_area_ratio(self, boxa, boxb):
        return 0.72


