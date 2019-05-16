#!/usr/bin/env python

## @package text_detection
#   
# @file evaluate.py
# 提取一幅图像的 MSER 选区
#   
# @author panderan@163.com 
#

from math import sqrt
import cv2
import matplotlib.pyplot as plt
import numpy as np

class evaluate:

    def __init__(self):
        pass

    def precision(self, boxes, ground_truth_img):
        # 提取真实文本区域的每个外接矩形
        gt_boxes = []
        image, contours, hierarchies = cv2.findContours(ground_truth_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for i, ctr in enumerate(contours):
            ro_rect = cv2.minAreaRect(ctr)
            box = np.int0(cv2.boxPoints(ro_rect))
            gt_boxes.append(box)
        
        # 计算精确度
        total_prec = 0.0
        for i,box in enumerate(boxes):
            # 寻找最匹配真实区域
            bins_box_img = np.zeros_like(ground_truth_img)
            bins_box_img = cv2.drawContours(bins_box_img, [np.int0(box)], 0, 255, cv2.FILLED)
            prec = 0.0

            bins_gt_box_img = np.zeros_like(ground_truth_img)
            for j, gt_box in enumerate(gt_boxes):
                # 计算交集
                bins_gt_box_img[:,:] = 0
                bins_gt_box_img = cv2.drawContours(bins_gt_box_img, [gt_box], 0, 255, cv2.FILLED)
                bins_gt_box_img = bins_gt_box_img & bins_box_img
                intersection_area_size = np.sum(bins_gt_box_img)/255.0

                # 无交集
                if intersection_area_size < 0.5:
                    continue
                
                # 计算准确度
                bins_gt_box_img[:,:] = 0
                bins_gt_box_img = cv2.drawContours(bins_gt_box_img, [gt_box], 0, 255, cv2.FILLED)
                bins_gt_box_img = bins_gt_box_img | bins_box_img
                union_area_size = np.sum(bins_gt_box_img)/255.0
                
                # 更新最大精确值
                if prec < intersection_area_size/union_area_size:
                    prec = intersection_area_size/union_area_size

            total_prec += prec
            prec = 0.0
        return total_prec/len(boxes)


    def recall(self, boxes, ground_truth_img):
        # 提取真实文本区域的每个外接矩形
        gt_boxes = []
        image, contours, hierarchies = cv2.findContours(ground_truth_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i, ctr in enumerate(contours):
            ro_rect = cv2.minAreaRect(ctr)
            box = np.int0(cv2.boxPoints(ro_rect))
            gt_boxes.append(box)

        total_recall = 0.0
        for i,gt_box in enumerate(gt_boxes):
            bins_gt_box_img = np.zeros_like(ground_truth_img)
            bins_gt_box_img = cv2.drawContours(bins_gt_box_img, [np.int0(gt_box)], 0, 255, cv2.FILLED)
            recall = 0.0

            bins_box_img = np.zeros_like(ground_truth_img)
            for j,box in enumerate(boxes):
                bins_box_img[:,:] = 0
                bins_box_img = cv2.drawContours(bins_box_img, [np.int0(box)], 0, 255, cv2.FILLED)
                bins_box_img = bins_box_img & bins_gt_box_img
                intersection_area_size = np.sum(bins_box_img) / 255.0

                if intersection_area_size < 0.5:
                    continue

                # 计算准确度
                bins_box_img[:,:] = 0
                bins_box_img = cv2.drawContours(bins_box_img, [np.int0(box)], 0, 255, cv2.FILLED)
                bins_box_img = bins_box_img | bins_gt_box_img
                union_area_size = np.sum(bins_box_img)/255.0

                if recall < intersection_area_size/union_area_size:
                    recall = intersection_area_size/union_area_size
            total_recall += recall
            recall = 0.0
        return total_recall/len(gt_boxes)
























