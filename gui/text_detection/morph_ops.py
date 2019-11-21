#!/usr/bin/env python

''' 图像形态学处理
'''

import cv2
import numpy as np


class TdMorphOperator:
    ''' 图像形态学处理类
    '''
    def __init__(self):
        self.k_erode = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        self.k_dilate = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))
        self.k_opening = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        self.k_closing = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    def morph_operation(self, mask_image, td_filter=None):
        ''' 对输入的二值图像进行形态学处理
            对二值图像中的每一个连通域进行先腐蚀后膨胀，如果腐蚀后连通域消失则略过
            腐蚀操作。然后进行闭运算和开运算
        '''
        _, contours, _ = cv2.findContours(mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        binary_image = np.uint8(np.zeros(mask_image.shape))
        ret_regions = []

        for i, ctr in enumerate(contours):
            binary_image[:, :] = 0
            binary_image = cv2.drawContours(binary_image, [ctr], 0, 255, thickness=cv2.FILLED)
            binary_image = self._morph_operation_once(binary_image)

            _, morphed_contours, _ = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            for morphed_ctr in morphed_contours:
                ro_rect = cv2.minAreaRect(morphed_ctr)
                pbox = np.int0(cv2.boxPoints(ro_rect))
                if td_filter is not None:
                    if not td_filter.validateRoRect(ro_rect):
                        continue
                ret_regions.append(pbox)

        return ret_regions

    def _morph_operation_once(self, binary_image):
        ''' 对输入的二值图像进行形态学处理，只处理一个连通域
        '''
        erode_image = cv2.erode(binary_image, self.k_erode)
        before_size = np.sum(binary_image)/255.0
        after_size = np.sum(erode_image)/255.0
        if after_size < 1.0:
            erode_image = binary_image
        if after_size/before_size < 1.0/9.0:
            erode_image = binary_image

        dilate_image = cv2.dilate(erode_image, self.k_dilate) if before_size < 500 else erode_image
        ret_image = cv2.morphologyEx(dilate_image, cv2.MORPH_CLOSE, self.k_closing)
        return ret_image

    def getMaskImage(self, mask_image, regions):
        ''' 获取 regions 掩码图
        '''
        regions_image = np.zeros_like(mask_image)
        for region in regions:
            cv2.drawContours(regions_image, [region], 0, 255, cv2.FILLED)
        return regions_image
