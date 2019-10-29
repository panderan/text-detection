#!/usr/bin/env python

'''
提取一幅图像的 MSER 选区
'''

from enum import Enum
import cv2
import numpy as np


class ExtractDirection(Enum):
    ''' 提取方向
    '''
    Positive = 1
    Negitive = 2
    Both = 4


class TdExtractConnectDomain:
    ''' MSER 连通域提取类
    从一幅灰度图像中提取 MSER 连通域
    '''
    def __init__(self):
        self.delta = 5
        self.min_area = 9
        self.max_area = 500
        self.variation = 0.25

    def extract(self, gray_image, flt=None, direction=ExtractDirection.Positive):
        ''' 提取 MSER 连通区域
        Args:
            flt 几何条件过滤实例，为 0 则不过滤
            direction MSER 提取方向，0 为 MSER+ ，1 为 MSER-
            channel 在指定通道上提取 MSERs
        Returns:
            retmsrs 候选连通域列表，每一个元素为包含了该连通域的所有点的列表
            retboxes 候选连通域列表，每一个元素包含了该连通域的外接矩形
        '''
        self.printParams()
        region_points, region_boxes = [], []
        mser = cv2.MSER_create(_delta=self.delta, _min_area=self.min_area, _max_area=self.max_area)
        if direction in (ExtractDirection.Positive, ExtractDirection.Both):
            points, boxes = mser.detectRegions(gray_image)
            region_points.extend(points)
            region_boxes.extend(boxes)
        if direction in (ExtractDirection.Negitive, ExtractDirection.Both):
            points, boxes = mser.detectRegions(255-gray_image)
            region_points.extend(points)
            region_boxes.extend(boxes)

        retpoints, retboxes = [], []
        if flt is not None:
            flt.gray_img = gray_image
            for (points, box) in zip(region_points, region_boxes):
                ret = flt.validate(points, box)
                if ret:
                    retpoints.append(points)
                    retboxes.append(box)
                else:
                    continue
        else:
            retpoints = region_points
            retboxes = region_boxes
        return retpoints, retboxes

    def extract_with_labels(self, gray_image, flt=None, direction=ExtractDirection.Positive):
        ''' 提取 MSER 连通区域（带标记）
        Args:
            flt 几何条件过滤实例，为 0 则不过滤
            direction MSER 提取方向，0 为 MSER+ ，1 为 MSER-
            channel 在指定通道上提取 MSERs
        Returns:
            rect_img 在原图中用矩形标出候选区域图像
            binarized 以背景图像为0，提取的连通域为255 的二值图像
        '''
        rect_image = gray_image.copy()
        binarized = np.zeros_like(gray_image)
        msers, bboxes = self.extract(gray_image, flt, direction)
        for i, box in enumerate(bboxes):
            rect_image = cv2.rectangle(rect_image, (box[0], box[1]), (box[0]+box[2], box[1]+box[3]), (255, 0, 0))
            binarized[msers[i][:, 1], msers[i][:, 0]] = 255
        return rect_image, binarized

    def extract_with_labels_for_images(self, gray_images, flt=None, direction=ExtractDirection.Positive):
        ''' 提取所有通道的 MSER，包括R，G，B，Gray
        Args:
            flt 几何条件过滤实例，为 0 则不过滤
            direction MSER 提取方向，0 为 MSER+ ，1 为 MSER-
            channel 在指定通道上提取 MSERs
        Returns:
            binarized 以背景图像为0，提取的连通域为255 的二值图像
        '''
        ret_binarized = None
        for gray_image in gray_images:
            _, binarized = self.extract_with_labels(gray_image, flt, direction)
            if ret_binarized is None:
                ret_binarized = binarized
            else:
                ret_binarized[binarized > 128] = binarized[binarized > 128]
        return ret_binarized

    def __setConfigItem(self, keystr, config):
        ''' 设置单个值
        '''
        try:
            if keystr == "delta":
                self.delta = config["delta"]
            elif keystr == "min_area":
                self.min_area = config["min_area"]
            elif keystr == "max_area":
                self.max_area = config["max_area"]
            elif keystr == "variation":
                self.variation = config["variation"]
            else:
                pass
        except KeyError:
            pass
        return

    def setConfig(self, config):
        ''' 设置配置文件
        '''
        if config is None:
            return
        self.__setConfigItem("delta", config)
        self.__setConfigItem("min_area", config)
        self.__setConfigItem("max_area", config)
        self.__setConfigItem("variation", config)
        return

    def printParams(self):
        ''' 打印当前参数
        '''
        params = {"delta": self.delta,
                  "min_area": self.min_area,
                  "max_area": self.max_area,
                  "variation": self.variation}
        print("Extract Params %s" % params)
