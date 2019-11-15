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
    DB_MAX = 6


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
        self.data = {'regions': [{'region':None, 'params':None, 'isVaild':True, 'private':None}],
                     'vertex0': {'x':[], 'y':[]},
                     'vertex1': {'x':[], 'y':[]},
                     'vertex2': {'x':[], 'y':[]},
                     'vertex3': {'x':[], 'y':[]}
                    }

    def initData(self, regions):
        ''' 初始化数据
        Args:
            regions: [[x,y], ...]
        '''
        for vtx_idx in range(4):
            for dimen in range(2):
                list_vertex = [[vertexs[vtx_idx][dimen], i] for i, vertexs in enumerate(regions)]
                list_vertex.sort(key=lambda v: v[0])
                list_key = [item[0] for item in list_vertex]
                keystr = "vertex" + str(vtx_idx)
                sub_keystr = "x" if dimen == 0 else "y"
                self.data[keystr][sub_keystr] = [list_key, list_vertex]
        self.data['regions'] = [{'region': region, 'params': None, 'isValid':True, 'private': None} for region in regions]

    def getRegionParams(self, idx):
        ''' 获取 region 参数
        '''
        region_item = self._getRegionItem(idx)
        if region_item is None:
            return None
        if  region_item['params'] is None:
            region_item['params'] = [None for i in range(MergingIdxDB.DB_MAX.value)]
            params = region_item['params']
            ro_rect = cv2.minAreaRect(np.array(region_item['region']))
            width, height, area_size = self.getRegionGeometry(ro_rect)
            params[MergingIdxDB.DB_WIDTH.value] = width
            params[MergingIdxDB.DB_HEIGHT.value] = height
            params[MergingIdxDB.DB_AREA_SIZE.value] = area_size
            angle = self.getRegionDirection(ro_rect)
            params[MergingIdxDB.DB_DIRECTION.value] = angle
            aspect_ratio = self.getRegionAspectRatio(ro_rect)
            params[MergingIdxDB.DB_ASPECT_RATIO.value] = aspect_ratio
            params[MergingIdxDB.DB_ROTATE_RECT.value] = ro_rect
            region_item['params'] = params
        return region_item['params']

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
        init_angle -= region_ro_rect[2]
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

        while len(item['private']) < pd_idx+1:
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

    def insertRegion(self, region):
        ''' 新增一个 region
        '''
        for vtx_idx in range(4):
            keystr = "vertex" + str(vtx_idx)
            for dimen in range(2):
                sub_keystr = "x" if dimen == 0 else "y"
                val = region[vtx_idx][dimen]
                inst_pos = bisect.bisect_left(self.data[keystr][sub_keystr][0], val)
                self.data[keystr][sub_keystr][0].insert(inst_pos, val)
                self.data[keystr][sub_keystr][1].insert(inst_pos, [val, len(self.data['regions'])])
        item = {"region": np.int64(region), "params":None, "private": None}
        self.data['regions'].append(item)

    def isRegionVaild(self, idx):
        ''' 检查一个 region 是否有效
        '''
        return self._getRegionItem(idx)['isValid']

    def deleteRegion(self, idx):
        ''' 删除一个 region
        '''
        self.data['regions'][idx]['isValid'] = False
        for vtx_idx in range(4):
            keystr = "vertex" + str(vtx_idx)
            for dimen in range(2):
                sub_keystr = "x" if dimen == 0 else "y"
                pos = [v[1] for v in self.data[keystr][sub_keystr][1]].index(idx)
                self.data[keystr][sub_keystr][0].pop(pos)
                self.data[keystr][sub_keystr][1].pop(pos)

    def getRegionLens(self, flag=0):
        ''' 获取region 列表的长度
        '''
        if flag:
            return sum([1 if v is not None else 0 for v in self.data['regions']])
        else:
            return len(self.data['regions'])

    def getAllRegionIds(self, flag=0):
        ''' 获取所有的 region ID
        Args:
            flag 0-所有， 1-仅有效region的ID
        '''
        ret_ids = []
        total = self.getRegionLens()
        for i in range(total):
            if self.isRegionVaild(i):
                ret_ids.append(i)
        return ret_ids

    def getNextRgionIdx(self, idx):
        ''' 获取下一个有效的 region ID
        '''
        total = self.getRegionLens()
        count = 0
        idx = idx+1 if idx+1 < len(self.data['regions']) else 0
        while not self.isRegionVaild(idx):
            count += 1
            if count == total:
                return -1
            idx = idx+1 if idx+1 < len(self.data['regions']) else 0
        return idx

    def getIdsInRange(self, keystr, xy_range):
        ''' 从 keystr 排序中获取指定范围的 region
        '''
        ranges = []
        region_ids = set()
        for dimen in range(2):
            sub_keystr = "x" if dimen == 0 else "y"
            start_idx = bisect.bisect_left(self.data[keystr][sub_keystr][0], xy_range[dimen][0])
            end_idx = bisect.bisect_left(self.data[keystr][sub_keystr][0], xy_range[dimen][1])
            ranges.append([self.data[keystr][sub_keystr][1][i][1] for i in range(start_idx, end_idx)])
        region_ids = region_ids.union(set(ranges[0]) & set(ranges[1]))
        return region_ids


class TdMergingDdebugData:
    ''' Debug 数据
    '''
    def __init__(self):
        self.enable = False
        self.data = {
            'original_regions': None,
            'elections': [{
                'cur_id': None,
                'candidate_ids':[0],
                'satisfied_items':[{
                    'init_ids': [],
                    'id': 0,
                    'compare_params':{
                        'position_ratio': 0
                    }
                }]
            }],
            'shape': None
        }
        self.data['elections'] = []

    def setOrignalRegions(self, regions):
        ''' 存入 original regions
        '''
        if not self.enable:
            return
        self.data['original_regions'] = regions

    def appendNewElection(self):
        ''' 新建一轮合并
        '''
        if not self.enable:
            return
        self.data['elections'].append({'init_ids':[], 'cur_id': None, 'candidate_ids': [], 'satisfied_items':[]})

    def setLastElection_InitIds(self, list_nums):
        ''' 设置
        '''
        self.data['elections'][-1]['init_ids'] = list_nums

    def setLastElection_CurId(self, num):
        ''' 设置最新一次合并的 cur id
        '''
        if not self.enable:
            return
        self.data['elections'][-1]['cur_id'] = num

    def setLastElection_CandidateIds(self, list_nums):
        ''' 设置最新一次合并的 candidate ids
        '''
        if not self.enable:
            return
        self.data['elections'][-1]['candidate_ids'] = list_nums

    def appendLastElection_NewSatisfied(self, idx):
        ''' 新增一个 satisfied region
        '''
        if not self.enable:
            return
        self.data['elections'][-1]['satisfied_items'].append({'id':idx, 'compare_params':{}})

    def setLastElection_LastSatisfiedItem(self, keyval_pair):
        ''' 设置最新一次合并的最新的 satisfied 的数据
        '''
        if not self.enable:
            return
        self.data['elections'][-1]['satisfied_items'][-1]['compare_params'][keyval_pair[0]] = keyval_pair[1]

    def getOriginalRegionData(self):
        ''' 获取原始数据
        '''
        return self.data['original_regions']

    def enableDebug(self, shape):
        ''' 启用 Debug 数据
        '''
        self.data['shape'] = shape
        self.enable = True

    def isEnable(self):
        ''' 是否启用
        '''
        return self.enable

    def getShape(self):
        ''' 获取 shape
        '''
        return self.data['shape']

    def getElection_InitRegionIds(self, elec_id):
        ''' 获取
        '''
        return self.data['elections'][elec_id]['init_ids']

    def getTotalElections(self):
        ''' 获取
        '''
        return len(self.data['elections'])

    def getElection_CurId(self, elec_id):
        ''' 获取
        '''
        return self.data['elections'][elec_id]['cur_id']

    def getElection_CandidateIds(self, elec_id):
        ''' 获取
        '''
        return self.data['elections'][elec_id]['candidate_ids']

    def getElection_TotalSatisfied(self, elec_id):
        ''' 获取
        '''
        return len(self.data['elections'][elec_id]['satisfied_items'])

    def getElection_SatisfiedId(self, elec_id, sat_id):
        ''' 获取
        '''
        return self.data['elections'][elec_id]['satisfied_items'][sat_id]['id']


class TdMergingTextLine:
    ''' 合并文本行
    '''
    def __init__(self):
        self.scope_lim = 25

        self.t_of_merged_areasize_lim = 20000       # 若合并后的大小超过此阈值则拒绝合并
        self.t_of_merged_aspect_lim = [0.0, 3.0]    # 若合并后的长宽比超过此阈值则拒绝合并
        self.t_of_overlap_ratio = 0.25
        self.t_of_distance = 2.6
        self.strategy = MergingStrategy.HORIZON.value

        self.data = TdMergingData()
        self.get_position_ratio_threshold = threshold_of_position_ratio_for_default
        self.get_dirtection_threshold = threshold_of_angle_for_default
        self.debug = TdMergingDdebugData()

    def mergeTextLine(self, regions):
        ''' 合并文本行
        '''
        self.data.initData(regions)
        self.debug.setOrignalRegions(self.data)

        max_loops = 1
        start_idx, loop_idx, restart_flag = 0, 0, True
        while max_loops > 0:
            if not restart_flag and loop_idx == start_idx:
                break
            ret_status = self.mergeTextLineOnce(self.data, loop_idx)
            if ret_status:
                start_idx = self.data.getRegionLens()
                loop_idx = start_idx
                restart_flag = True
            else:
                loop_idx = self.data.getNextRgionIdx(loop_idx)
                if loop_idx < 0:
                    break
                restart_flag = False
            max_loops -= 1

    def mergeTextLineOnce(self, data, cur_id):
        ''' 一次合并
        '''
        # 选举出待合并 region
        region_ids = self._selectCandidate(data, cur_id)
        self.debug.appendNewElection()
        self.debug.setLastElection_InitIds(data.getAllRegionIds(flag=1))
        self.debug.setLastElection_CurId(cur_id)
        self.debug.setLastElection_CandidateIds(region_ids)
        if len(region_ids) == 0:
            return False

        # 选出满足条件的待合并 region
        satisfied_candidate = []
        for candidate_id in region_ids:
            if self._compare2Regions(data, cur_id, candidate_id):
                satisfied_candidate.append(candidate_id)
        if len(satisfied_candidate) == 0:
            return False

        # 寻找本次合并的 region
        best_id = self._pickUpBestCandidate(data, cur_id, satisfied_candidate)
        if best_id is None:
            return False

        merged_id = self._mergeTowRegions(data, cur_id, best_id)
        return merged_id

    def _selectCandidate(self, data, idx):
        ''' 产生候选者
        '''
        region = data.getRegionVertexs(idx)
        ro_rect = cv2.minAreaRect(region)
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
            region_ids = region_ids.union(data.getIdsInRange(keystr, xy_range))

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
        return best_id[1]

    def _mergeTowRegions(self, data, id1, id2):
        ''' 合并两个 region
        '''
        joint_ro_rect = cv2.minAreaRect(np.vstack((data.getRegionVertexs(id1), data.getRegionVertexs(id2))))
        joint_region = cv2.boxPoints(joint_ro_rect)
        data.deleteRegion(id1)
        data.deleteRegion(id2)
        data.insertRegion(joint_region)
        return data.getRegionLens()-1

    def _compare2Regions(self, data, id1, id2):
        ''' 比较两个区域是否可以合并
        '''
        region1_params = data.getRegionParams(id1)
        region2_params = data.getRegionParams(id2)
        if region1_params is None or region2_params is None:
            return False

        self.debug.appendLastElection_NewSatisfied(id2)

        # 判断合并后面积
        joint_ro_rect = cv2.minAreaRect(np.vstack((data.getRegionVertexs(id1), data.getRegionVertexs(id2))))
        _, _, joint_area_size = TdMergingData.getRegionGeometry(joint_ro_rect)
        self.debug.setLastElection_LastSatisfiedItem(('joint_area_size', joint_area_size))
        if joint_area_size > self.t_of_merged_areasize_lim:
            return False

        # 判断合并后宽高比
        joint_aspect_ratio = data.getRegionAspectRatio(joint_ro_rect)
        self.debug.setLastElection_LastSatisfiedItem(('joint_aspect_ratio', joint_aspect_ratio))
        if not is_in_range(joint_aspect_ratio, self.t_of_merged_aspect_lim):
            return False

        # 判断两个 region 的重叠率
        overlap_ratio = self._getOverlapRatio(data, id1, id2)
        self.debug.setLastElection_LastSatisfiedItem(('overlap_ratio', overlap_ratio))
        if overlap_ratio > self.t_of_overlap_ratio:
            return False

        # 判断两个 region 的位置比率
        position_ratio = (data.getParamAreaSize(id1) + data.getParamAreaSize(id2)) / joint_area_size
        data.savePrivateData(id2, 0, position_ratio)    # id2 为候选者ID
        self.debug.setLastElection_LastSatisfiedItem(('position_ratio', position_ratio))
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

        all_vertexs = np.vstack((data.getRegionVertexs(id1), data.getRegionVertexs(id2)))
        low_x, high_x = min([i[0] for i in all_vertexs]), max([i[0] for i in all_vertexs])
        low_y, high_y = min([i[1] for i in all_vertexs]), max([i[1] for i in all_vertexs])
        shift_vertexs1 = [[v[0]-low_x, v[1]-low_y] for v in data.getRegionVertexs(id1)]
        shift_vertexs2 = [[v[0]-low_x, v[1]-low_y] for v in data.getRegionVertexs(id2)]

        mask_region1 = np.zeros((high_x-low_x, high_y-low_y))
        mask_region2 = np.zeros((high_x-low_x, high_y-low_y))
        mask_region1 = np.int64(cv2.drawContours(mask_region1, [np.array(shift_vertexs1)], 0, 255, cv2.FILLED))
        mask_region2 = np.int64(cv2.drawContours(mask_region2, [np.array(shift_vertexs2)], 0, 255, cv2.FILLED))
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
        self.debug.setLastElection_LastSatisfiedItem(('direction', [dir1, dir2, centerline_dir, threshold, dir_type, ret1, ret2]))

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

        all_vertexs = np.vstack((data.getRegionVertexs(id1), data.getRegionVertexs(id2)))
        low_x, high_x = min([i[0] for i in all_vertexs]), max([i[0] for i in all_vertexs])
        low_y, high_y = min([i[1] for i in all_vertexs]), max([i[1] for i in all_vertexs])
        shift_vertexs1 = [[v[0]-low_x, v[1]-low_y] for v in data.getRegionVertexs(id1)]
        shift_vertexs2 = [[v[0]-low_x, v[1]-low_y] for v in data.getRegionVertexs(id2)]

        mask_region1 = np.uint8(np.zeros((high_x-low_x, high_y-low_y)))
        mask_region1 = cv2.drawContours(mask_region1, [np.array(shift_vertexs1)], 0, 255, cv2.FILLED)
        mask_region1 = cv2.morphologyEx(mask_region1, cv2.MORPH_DILATE, kel)
        mask_region1 = cv2.drawContours(mask_region1, [np.array(shift_vertexs2)], 0, 255, cv2.FILLED)
        _, contours, _ = cv2.findContours(np.uint8(mask_region1), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        retval = bool(len(contours) == 1)
        self.debug.setLastElection_LastSatisfiedItem(('distance', [kel_size, retval]))
        return retval

    def _judgeStrategy(self, data, id1, id2):
        ''' 判断两个 region 的策略是否满足
            水平策略会拒绝合并明显具有垂直关系的两个 regioon，反之亦然
        '''
        center_vertex1 = data.getRegionCenterVertex(id1)
        center_vertex2 = data.getRegionCenterVertex(id2)

        if self.strategy & MergingStrategy.HORIZON.value:
            _, _, width1, _ = cv2.boundingRect(data.getRegionVertexs(id1))
            _, _, width2, _ = cv2.boundingRect(data.getRegionVertexs(id2))
            threshold = width1 if width1 > width2 else width2
            retval = bool(abs(center_vertex1[0]-center_vertex2[0]) > threshold/2.0)
            self.debug.setLastElection_LastSatisfiedItem(('strategy', [center_vertex1[0], center_vertex2[0], threshold, self.strategy, retval]))
            return retval

        if self.strategy & MergingStrategy.VERTICAL.value:
            _, _, _, height1 = cv2.boundingRect(data.getReionVertex(id1))
            _, _, _, height2 = cv2.boundingRect(data.getReionVertex(id2))
            threshold = height1 if height1 > height2 else height2
            retval = bool(abs(center_vertex1[1]-center_vertex2[1]) > threshold/2.0)
            self.debug.setLastElection_LastSatisfiedItem(('strategy', [center_vertex1[1], center_vertex2[1], threshold, self.strategy, retval]))
            return retval
        return True


def threshold_of_position_ratio_for_default(data, id1, id2):
    ''' 默认 position ratio 的阈值
    '''
    return 0.7


def threshold_of_angle_for_default(data, id1, id2):
    ''' 默认 direction 的阈值
    '''
    threshold = 30
    return [threshold, 90-threshold]


def debugGenerateElectionImage(debug_data, elec_id):
    ''' 生成 Vebose 图像
    '''
    shape = debug_data.getShape()
    image = np.uint8(np.zeros((shape[0], shape[1], 3)))

    # 底图
    org_data = debug_data.getOriginalRegionData()
    for i in debug_data.getElection_InitRegionIds(elec_id):
        region = org_data.getRegionVertexs(i)
        image = cv2.drawContours(image, [region], 0, (128, 128, 128), cv2.FILLED)

    # 所有候选者
    i = 0
    candidate_ids = debug_data.getElection_CandidateIds(elec_id)
    while i < len(candidate_ids):
        region = org_data.getRegionVertexs(candidate_ids[i])
        image = cv2.drawContours(image, [region], 0, (128, 0, 0), cv2.FILLED)
        i += 1

    # 所有满足者
    for i in range(debug_data.getElection_TotalSatisfied(elec_id)):
        region = org_data.getRegionVertexs(debug_data.getElection_SatisfiedId(elec_id, i))
        image = cv2.drawContours(image, [region], 0, (255, 0, 0), cv2.FILLED)

    # 中心者
    idx = debug_data.getElection_CurId(elec_id)
    region = org_data.getRegionVertexs(idx)
    image = cv2.drawContours(image, [region], 0, (0, 0, 255), cv2.FILLED)

    return image
