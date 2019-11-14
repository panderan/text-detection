#!/usr/bin/env python

''' @package text_detection
    提取连通域边界模块
'''

from enum import Enum
import bisect
import math
import numpy as np
import cv2
from gui.text_detection.common import is_in_range


class MergingIdxDB(Enum):
    ''' 数据下标索引
    '''
    DB_WIDTH = 0
    DB_HEIGHT = 1
    DB_AREA_SIZE = 2
    DB_DIRECTION = 3
    DB_ASPECT_RATIO = 4
    DB_ROTATE_RECT = 5


class MergingIdxJDG(Enum):
    ''' JDG 索引
    '''
    JDG_UNKONWN = 0
    JDG_DISALLOW = 1
    JDG_ALLOWED = 2


class MergingFlagDirt(Enum):
    ''' Direction 标示
    '''
    DIRECTION_TYPE_NONE = 1
    DIRECTION_TYPE_PARALLEL = 2
    DIRECTION_TYPE_VERTICAL = 4


class MergingStrategy(Enum):
    ''' 策略标识
    '''
    HORIZON = 1
    VERTICAL = 2


class TdMergingData:
    ''' 文本行合并数据结构
    '''
    def __init__(self):
        self.enable_aspect_ratio_gt1 = True
        self.data = {"regions": [{"region":None, "params":None, "private":None}],
                     "vertex0": {"x":[], "y":[]},
                     "vertex1": {"x":[], "y":[]},
                     "vertex2": {"x":[], "y":[]},
                     "vertex3": {"x":[], "y":[]}
                    }

    def initData(self, regions):
        ''' 初始化数据
        '''
        for vtx_idx in range(4):
            for dimen in range(2):
                list_vertex = [[vertexs[vtx_idx][dimen], i] for i, vertexs in enumerate(regions)]
                list_vertex.sort(key=lambda v: v[0])
                list_key = [item[0] for item in list_vertex]
                keystr = "vertex" + str(vtx_idx)
                sub_keystr = "x" if dimen == 0 else "y"
                self.data[keystr][sub_keystr] = [list_key, list_vertex]

    def getRegionParams(self, idx):
        ''' 获取 region 参数
        '''
        params = []
        region = self._getRegionItem(idx)
        if region is None:
            return None
        if  region['params'] is None:
            ro_rect = cv2.minAreaRect(np.array(region))
            width, height, area_size = self.getRegionGeometry(ro_rect)
            params[MergingIdxDB.DB_WIDTH.value] = width
            params[MergingIdxDB.DB_HEIGHT.value] = height
            params[MergingIdxDB.DB_AREA_SIZE.value] = area_size
            angle = self.getRegionDirection(ro_rect)
            params[MergingIdxDB.DB_DIRECTION.value] = angle
            aspect_ratio = self.getRegionAspectRatio(ro_rect)
            params[MergingIdxDB.DB_ASPECT_RATIO.value] = aspect_ratio
            params[MergingIdxDB.DB_ROTATE_RECT.value] = ro_rect
            region['params'] = params
        return region['params']

    def _getRegionItem(self, idx):
        ''' 获取指定 id 的 region 数据字典
        '''
        return self.data['regions'][idx]

    @staticmethod
    def getRegionGeometry(region_ro_rect):
        ''' 返回 region 的长宽面积
        '''
        return region_ro_rect[1][0], \
               region_ro_rect[1][1], \
               region_ro_rect[1][0] * region_ro_rect[1][1]

    @staticmethod
    def getRegionDirection(region_ro_rect):
        ''' 返回 region 的方向
        '''
        init_angle = 0 if region_ro_rect[1][0] > region_ro_rect[1][1] else 90
        init_angle -= region_ro_rect[3]
        return init_angle

    def getRegionAspectRatio(self, region_ro_rect):
        ''' 返回 region 长宽比
        '''
        aspect_ratio = region_ro_rect[1][0] / region_ro_rect[1][1]
        if self.enable_aspect_ratio_gt1 and aspect_ratio < 1.0:
            aspect_ratio = 1.0 / aspect_ratio
        return aspect_ratio

    def getRegionVertexs(self, idx):
        ''' 获取指定 id 的 region 的顶点
        '''
        return self._getRegionItem(idx)['region']

    def getParamWidth(self, idx):
        ''' 获取指定 id 的 region 的宽度
        '''
        return self.getRegionParams(idx)[MergingIdxDB.DB_WIDTH.value]

    def getParamHeight(self, idx):
        ''' 获取指定 id 的 region 的高度
        '''
        return self.getRegionParams(idx)[MergingIdxDB.DB_HEIGHT.value]

    def getParamAreaSize(self, idx):
        ''' 获取指定 id 的 region 的面积
        '''
        return self.getRegionParams(idx)[MergingIdxDB.DB_AREA_SIZE.value]

    def getParamAspectRatio(self, idx):
        ''' 获取指定 id 的 region 的高宽比
        '''
        return self.getRegionParams(idx)[MergingIdxDB.DB_ASPECT_RATIO.value]

    def getParamDirection(self, idx):
        ''' 获取指定 id 的 region 的方向
        '''
        return self.getRegionParams(idx)[MergingIdxDB.DB_DIRECTION.value]

    def getRegionCenterVertex(self, idx):
        ''' 获取 region 的中心坐标点
        '''
        return self.getRegionParams(idx)[MergingIdxDB.DB_ROTATE_RECT.value][0]

    def isMultiCharRegion(self, idx):
        ''' 指定区域是否是多字符区域
        '''
        if self.getParamAreaSize(idx) > 2000:
            return True
        if self.getParamWidth(idx) > 60 or self.getParamHeight(idx) > 60:
            return True
        return False

    def savePrivateData(self, idx, pd_idx, value):
        ''' 在 id 为 idx 的 region 中存入 id 为 pd_idx 的私有数据
            私有数据用列表存放
        '''
        item = self._getRegionItem(idx)
        if item['private'] is None:
            item['private'] = []

        while len(item['private']) < pd_idx:
            item['private'].append(None)
        item['private'][pd_idx] = value

    def getPrivateData(self, idx, pd_idx):
        ''' 读取 id 为 idx 的 region 中 id 为 pd_idx 的私有数据
        '''
        item = self._getRegionItem(idx)
        if len(item['private']) > pd_idx:
            return item['private'][pd_idx]
        else:
            return None



class TdMergingTextLine:
    ''' 合并文本行
    '''
    def __init__(self):
        self.scope_lim = 25
        self.last_merge_id = 0

        self.t_of_merged_areasize_lim = 20000       # 若合并后的大小超过此阈值则拒绝合并
        self.t_of_merged_aspect_lim = [0.0, 3.0]    # 若合并后的长宽比超过此阈值则拒绝合并
        self.t_of_overlap_ratio = 0.25
        self.t_of_distance = 2.6
        self.strategy = MergingStrategy.HORIZON.value

        self.data = TdMergingData()
        self.get_position_ratio_threshold = threshold_of_position_ratio_for_default
        self.get_dirtection_threshold = threshold_of_angle_for_default
        self.debug_data = {}
        self.debug_enable = False

    def mergeTextLine(self, regions):
        ''' 合并文本行
        '''
        self.data.initData(regions)
        while self.mergeTextLineOnce(self.data):
            pass

    def mergeTextLineOnce(self, data, pos=-1):
        ''' 一次合并
        '''
        # 选举出待合并区域
        cur_id = self.last_merge_id if pos == -1 else pos
        region_ids = self._selectCandidate(data, cur_id)
        if self.debug_enable:
            self.debug_data['elections'].append({"ids":region_ids, "cur_id": cur_id})

        satisfied_candidate = []
        for candidate_id in region_ids:
            if self._compare2Regions(data, cur_id, candidate_id):
                satisfied_candidate.append(candidate_id)

        best_id = self._pickUpBestCandidate(data, cur_id, satisfied_candidate)

        return False

    def _selectCandidate(self, data, idx):
        ''' 产生候选者
        '''
        region = data['regions'][idx]['region']
        ro_rect = cv2.minAreaRect(np.array(region))
        extend_ro_rect = (ro_rect[0], \
                          (ro_rect[1][0]+self.scope_lim, ro_rect[1][1]+self.scope_lim), \
                          ro_rect[2])
        scope_region = cv2.boxPoints(extend_ro_rect)
        x_range = [min([x for x in scope_region[:, 0]]), max([x for x in scope_region[:, 0]])+1]
        y_range = [min([y for y in scope_region[:, 1]]), max([y for y in scope_region[:, 1]])+1]
        xy_range = [x_range, y_range]

        region_ids = set()
        for vtx_idx in range(4):
            keystr = "vertex" + str(vtx_idx)
            ranges = []
            for dimen in range(2):
                sub_keystr = "x" if dimen == 0 else "y"
                start_idx = bisect.bisect_left(data[keystr][sub_keystr][0], xy_range[dimen][0])
                end_idx = bisect.bisect_left(data[keystr][sub_keystr][0], xy_range[dimen][1])
                ranges.append([i for i in range(start_idx, end_idx)])
            region_ids = region_ids.union(set(ranges[0]) & set(ranges[1]))

        return list(region_ids)

    def _pickUpBestCandidate(self, data, cur_id, ids):
        ''' 选出最合适的候选 region
        '''
        vals = []
        best_id = None
        cur_center_vertex = data.getRegionCenterVertex(cur_id)
        for idx in ids:
            center_vertex = data.getRegionCenterVertex(idx)
            if self.strategy & MergingStrategy.HORIZON.value:
                vals.append([abs(center_vertex[0]-cur_center_vertex[0]), idx])
            elif self.strategy & MergingStrategy.VERTICAL.value:
                vals.append([abs(center_vertex[1]-cur_center_vertex[1]), idx])
            else:
                val = data.getPrivateData(idx, 0)
                if val is not None:
                    vals.append([val, idx])
        best_id = max(vals, key=lambda v: v[0])
        return best_id

    def _mergeTowRegions(self, id1, id2):
        ''' 合并两个 region
        '''
        pass

    def _compare2Regions(self, data, id1, id2):
        ''' 比较两个区域是否可以合并
        '''
        region1_params = data.getRegionParams(id1)
        region2_params = data.getRegionParams(id2)
        if region1_params is None or region2_params is None:
            return False

        # 判断合并后面积
        joint_ro_rect = cv2.minAreaRect(np.array(data.getRegionVertexs(id1) + data.getRegionVertexs(id2)))
        _, _, joint_area_size = TdMergingData.getRegionGeometry(joint_ro_rect)
        if joint_area_size > self.t_of_merged_areasize_lim:
            return False

        # 判断合并后宽高比
        joint_aspect_ratio = data.getRegionAspectRatio(joint_ro_rect)
        if not is_in_range(joint_aspect_ratio, self.t_of_merged_aspect_lim):
            return False

        # 判断两个 region 的重叠率
        overlap_ratio = self._getOverlapRatio(data, id1, id2)
        if overlap_ratio > self.t_of_overlap_ratio:
            return False

        # 判断两个 region 的位置比率
        position_ratio = (data.getParamAreaSize(id1) + data.getParamAreaSize(id2)) / joint_area_size
        data.savePrivateData(id2, 0, position_ratio)    # id2 为候选者ID
        if position_ratio < self.get_position_ratio_threshold(data, id1, id2):
            return False

        if self._judgeDirection(data, id1, id2) \
            and self._judgeDistance(data, id1, id2) \
            and self._judgeStrategy(data, id1, id2):
            return True
        return False

    def _getOverlapRatio(self, data, id1, id2):
        ''' 计算两个 region 的重叠率
        '''
        area_size1 = data.getParamAreaSize(id1)
        area_size2 = data.getParamAreaSize(id2)
        min_area_size = area_size1 if area_size1 < area_size2 else area_size2

        all_vertexs = data.getRegionVertexs(id1) + data.getRegionVertexs(id2)
        low_x, high_x = min([i[0] for i in all_vertexs]), max([i[0] for i in all_vertexs])
        low_y, high_y = min([i[1] for i in all_vertexs]), max([i[1] for i in all_vertexs])
        shift_vertexs1 = [[v[0]-low_x, v[1]-low_y] for v in data.getRegionVertexs(id1)]
        shift_vertexs2 = [[v[0]-low_x, v[1]-low_y] for v in data.getRegionVertexs(id2)]

        mask_region1 = np.zeros((high_x-low_x, high_y-low_y))
        mask_region2 = np.zeros((high_x-low_x, high_y-low_y))
        mask_region1 = cv2.drawContours(mask_region1, [shift_vertexs1], 0, 255, cv2.FILLED)
        mask_region2 = cv2.drawContours(mask_region2, [shift_vertexs2], 0, 255, cv2.FILLED)
        return np.sum(mask_region1 & mask_region2)/min_area_size

    def _getCenterLineDirection(self, data, id1, id2):
        ''' 计算两个 region 中心点的连线
        '''
        center_vertex1 = np.array(data.getRegionCenterVertex(id1))
        center_vertex2 = np.array(data.getRegionCenterVertex(id2))
        centers_vector = np.int16(center_vertex1 - center_vertex2)
        if centers_vector[0] < 0:
            centers_vector *= -1
        if centers_vector[0] == 0:
            return 90 if centers_vector[1] > 0 else -90
        angle = math.degrees(math.atan(centers_vector[1]/centers_vector[0]))
        return angle

    def _isAngleSatisfy(self, angle, threshold, flag):
        ''' 检测夹角是否满足平行或垂直条件
        '''
        if flag & MergingFlagDirt.DIRECTION_TYPE_PARALLEL:
            if angle > threshold[0]:
                if flag & MergingFlagDirt.DIRECTION_TYPE_VERTICAL and angle < threshold[1]:
                    return False
                else:
                    return True
            return False
        return True

    def _judgeDirection(self, data, id1, id2):
        ''' 判断两个 region 的方向是否满足
        '''
        # 若两个都是字符区域则忽略方向判断
        if not data.isMultiCharRegion(id1) and not data.isMultiCharRegion(id2):
            return True

        dir_type = MergingFlagDirt.DIRECTION_TYPE_PARALLEL.value
        if data.getParamAspectRatio(id1) < 1.5 or data.getParamAspectRatio(id2) < 1.5:
            dir_type |= MergingFlagDirt.DIRECTION_TYPE_VERTICAL.value

        dir1 = data.getParamDirection(id1)
        dir2 = data.getParamDirection(id2)
        centerline_dir = self._getCenterLineDirection(data, id1, id2)
        test_angle1 = min([abs(centerline_dir-dir1), abs(centerline_dir-((dir1+180)%360))])
        test_angle2 = min([abs(centerline_dir-dir2), abs(centerline_dir-((dir2+180)%360))])
        threshold = self.get_dirtection_threshold(data, id1, id2)
        ret1 = self._isAngleSatisfy(test_angle1, threshold, dir_type)
        ret2 = self._isAngleSatisfy(test_angle2, threshold, dir_type)
        if not ret1 and not ret2:
            return False

        if data.isMultiCharRegion(id1) and data.isMultiCharRegion(id2):
            test_angle1 = min([abs(dir1-dir2), abs(dir1-((dir2+180)%360))])
            ret1 = self._isAngleSatisfy(test_angle1, threshold, dir_type)
            if not ret1:
                return False
        return True

    def _judgeDistance(self, data, id1, id2):
        ''' 判断两个 region 的距离是否满足
        '''
        area_size1 = data.getParamAreaSize(id1)
        area_size2 = data.getParamAreaSize(id2)
        min_area_size = area_size1 if area_size1 < area_size2 else area_size2
        kel_size = int(math.sqrt(min_area_size*self.t_of_distance)*2)
        kel = cv2.getStructuringElement(cv2.MORPH_RECT, (kel_size, kel_size))

        all_vertexs = data.getRegionVertexs(id1) + data.getRegionVertexs(id2)
        low_x, high_x = min([i[0] for i in all_vertexs]), max([i[0] for i in all_vertexs])
        low_y, high_y = min([i[1] for i in all_vertexs]), max([i[1] for i in all_vertexs])
        shift_vertexs1 = [[v[0]-low_x, v[1]-low_y] for v in data.getRegionVertexs(id1)]
        shift_vertexs2 = [[v[0]-low_x, v[1]-low_y] for v in data.getRegionVertexs(id2)]

        mask_region1 = np.zeros((high_x-low_x, high_y-low_y))
        mask_region1 = cv2.drawContours(mask_region1, [shift_vertexs1], 0, 255, cv2.FILLED)
        mask_region1 = cv2.morphologyEx(mask_region1, cv2.MORPH_DILATE, kel)
        mask_region1 = cv2.drawContours(mask_region1, [shift_vertexs2], 0, 255, cv2.FILLED)

        _, contours, _ = cv2.findContours(mask_region1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        return bool(len(contours) == 1)

    def _judgeStrategy(self, data, id1, id2):
        ''' 判断两个 region 的策略是否满足
            水平策略会拒绝合并明显具有垂直关系的两个 regioon，反之亦然
        '''
        center_vertex1 = data.getRegionCenterVertex(id1)
        center_vertex2 = data.getRegionCenterVertex(id2)

        if self.strategy & MergingStrategy.HORIZON.value:
            width1 = cv2.boundingRect(data.getReionVertex(id1))
            width2 = cv2.boundingRect(data.getReionVertex(id2))
            threshold = width1 if width1 > width2 else width2
            return bool(abs(center_vertex1[0]-center_vertex2[0]) > threshold/2.0)
        
        if self.strategy & MergingStrategy.VERTICAL.value:
            height1 = cv2.boundingRect(data.getReionVertex(id1))
            height2 = cv2.boundingRect(data.getReionVertex(id2))
            threshold = height1 if height1 > height2 else height2
            return bool(abs(center_vertex1[1]-center_vertex2[1]) > threshold/2.0)
        return True

    @property
    def debug_enable(self):
        ''' 启用 debug
        debug_data 必须有 shape 键值对
        '''
        return self.__debug_enable
    @debug_enable.setter
    def debug_enable(self, val):
        if not val:
            self.__debug_enable = False
        else:
            try:
                if len(self.debug_data['shape']) == 2:
                    self.__debug_enable = True
            except KeyError:
                pass


def threshold_of_position_ratio_for_default(data, id1, id2):
    ''' 默认 position ratio 的阈值
    '''
    return 0.7


def threshold_of_angle_for_default(data, id1, id2):
    ''' 默认 direction 的阈值
    '''
    threshold = 30
    return [threshold, 90-threshold]


def debugGenerateElectionImage(debug_data, idx):
    ''' 生成 Vebose 图像
    '''
    image = np.zeros((debug_data['shape'][0], debug_data['shape'][1], 3))
    election = debug_data['elections'][idx]

    for item in debug_data['original_regions']:
        region = item['region']
        image = cv2.drawContours(image, [region], 0, (128, 128, 128), cv2.FILLED)

    for item in election['ids']:
        elect_region = debug_data['original_regions'][item]['region']
        image = cv2.drawContours(image, [elect_region], 0, (255, 0, 0), cv2.FILLED)

    image = cv2.drawContours(image, \
                             [debug_data['original_regions'][election['cur_id']]['region']], \
                             0, (0, 255, 0), cv2.FILLED)
    return image
