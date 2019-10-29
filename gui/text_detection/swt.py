#!/usr/bin/env python

'''计算一幅灰度图像中的所有笔画宽度和相关统计值
'''

import cv2
import numpy as np
from scipy.stats import mode, norm
from text_detection.common import common as comm

class swt:
    ''' SWT 算法
    '''
    def __init__(self):

        self.step_lim = 10              # 迭代次数限制
        self.direction = "both"         # 查找方向
        self.gray_image = None          # 输入的灰度图像
        self.canny_image = None         # Canny 边缘图像
        self.sobelX = None
        self.sobelY = None
        self.stepsX = None
        self.stepsY = None
        self.magnitudes = None
        self.gradsX = None
        self.gradsY = None

    def get_stroke_properties(self, stroke_widths):
        ''' 计算笔画宽度的统计值
        Args:
            stroke_widths: 笔画宽度数据
        Return:
            （众数值，众数个数，均值，标准差，最小值，最大值）
        '''
        if len(stroke_widths) == 0:
            return (0, 0, 0, 0, 0, 0)
        try:
            most_stroke_width = mode(stroke_widths, axis=None)[0][0]    ## Most probable stroke width is the most one
            most_stroke_width_count = mode(stroke_widths, axis=None)[1][0]  ## Most probable stroke width is the most one
        except IndexError:
            most_stroke_width = 0
            most_stroke_width_count = 0
        try:
            mean, std = norm.fit(stroke_widths)
            xMin, xMax = int(min(stroke_widths)), int(max(stroke_widths))
        except ValueError:
            mean, std, xMin, xMax = 0, 0, 0, 0
        return (most_stroke_width, most_stroke_width_count, mean, std, xMin, xMax)

    def get_strokes(self, xywh):
        ''' 计算所有边缘点的笔画宽度
        Args:
            xywh: 需要计算的区域
        Returns:
            笔画宽度数据
        '''
        x, y, w, h = xywh
        stroke_widths = np.array([[np.Infinity, np.Infinity]])
        for i in range(y, y + h):
            for j in range(x, x + w):
                if self.canny_image[i, j] != 0:
                    gradX = self.gradsX[i, j]
                    gradY = self.gradsY[i, j]
                    prevX, prevY, prevX_opp, prevY_opp, step_size = i, j, i, j, 0

                    if self.direction == "light":
                        go, go_opp = True, False
                    elif self.direction == "dark":
                        go, go_opp = False, True
                    else:
                        go, go_opp = True, True

                    stroke_width = np.Infinity
                    stroke_width_opp = np.Infinity
                    while (go or go_opp) and (step_size < self.step_lim):
                        step_size += 1

                        if go:
                            curX = np.int(np.floor(i + gradX * step_size))
                            curY = np.int(np.floor(j + gradY * step_size))
                            if (curX <= y or curY <= x or curX >= y + h or curY >= x + w):
                                go = False
                            if go and ((curX != prevX) or (curY != prevY)):
                                try:
                                    if self.canny_image[curX, curY] != 0:
                                        if np.arccos(gradX * -self.gradsX[curX, curY] + gradY * -self.gradsY[curX, curY]) < np.pi/2.0:
                                            # 若两个方向是相对的，则计算其距离
                                            stroke_width = int(np.sqrt((curX - i) ** 2  + (curY - j) ** 2))
                                            go = False
                                except IndexError:
                                    go = False
                                prevX = curX
                                prevY = curY

                        if go_opp:
                            curX_opp = np.int(np.floor(i - gradX * step_size))
                            curY_opp = np.int(np.floor(j - gradY * step_size))
                            if (curX_opp <= y or curY_opp <= x or curX_opp >= y + h or curY_opp >= x + w):
                                go_opp = False
                            if go_opp and ((curX_opp != prevX_opp) or (curY_opp != prevY_opp)):
                                try:
                                    if self.canny_image[curX_opp, curY_opp] != 0:
                                        if np.arccos(gradX * -self.gradsX[curX_opp, curY_opp] + gradY * -self.gradsY[curX_opp, curY_opp]) < np.pi/2.0:
                                            stroke_width_opp = int(np.sqrt((curX_opp - i) ** 2  + (curY_opp - j) ** 2))
                                            go_opp = False
                                except IndexError:
                                    go_opp = False
                                prevX_opp = curX_opp
                                prevY_opp = curY_opp

                    stroke_widths = np.append(stroke_widths, [(stroke_width, stroke_width_opp)], axis=0)

        stroke_widths_opp = np.delete(stroke_widths[:, 1], np.where(stroke_widths[:, 1] == np.Infinity))
        stroke_widths = np.delete(stroke_widths[:, 0], np.where(stroke_widths[:, 0] == np.Infinity))
        return stroke_widths, stroke_widths_opp

    def setImage(self, gray_image):
        ''' 设置待处理图像
        '''
        self.gray_image = gray_image
        self.canny_image = comm.apply_canny(self.gray_image)
        # Sobel算子的数学定义 http://blog.sciencenet.cn/blog-425437-1139187.html
        self.sobelX = cv2.Sobel(self.gray_image, cv2.CV_64F, 1, 0, ksize=-1)
        self.sobelY = cv2.Sobel(self.gray_image, cv2.CV_64F, 0, 1, ksize=-1)
        self.stepsX = self.sobelY.astype(int)  ## Steps are inversed!! (x-step -> sobelY)
        self.stepsY = self.sobelX.astype(int)
        self.magnitudes = np.sqrt(self.stepsX * self.stepsX + self.stepsY * self.stepsY)
        self.gradsX = self.stepsX / (self.magnitudes + 1e-10)
        self.gradsY = self.stepsY / (self.magnitudes + 1e-10)
