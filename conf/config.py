#!/usr/bin/env python

''' 读取配置文件
'''

import sys
import yaml
from gui.text_detection.region_filter import TdFilterCheckType

class TdPrepConfig:
    ''' 预处理参数
    '''
    def __init__(self, yaml_config=None):
        self.total_pixels = 400000
        self.canny_max = 0.9
        self.canny_min = 0.7
        self.gamma = 3.0
        self.sigmod_center = 0.7
        self.sigmod_zoom = 5
        self.struct_element_size = 5
        self.gauss_blur_size = 51
        self.hat = 1
        if yaml_config is not None:
            self.setConfig(yaml_config)

    def setConfig(self, yaml_config):
        ''' 设置配置文件
        '''
        yaml_prep_config = yaml_config['prep']
        self.total_pixels = int(yaml_prep_config['total_pixels'])
        self.gamma = float(yaml_prep_config['gamma'])
        self.struct_element_size = int(yaml_prep_config['struct_element_size'])
        self.gauss_blur_size = int(yaml_prep_config['gauss_blur_size'])
        self.sigmod_center = float(yaml_prep_config['sigmod'][0])
        self.sigmod_zoom = float(yaml_prep_config['sigmod'][1])
        self.canny_max = float(yaml_prep_config['canny'][0])
        self.canny_min = float(yaml_prep_config['canny'][1])
        self.hat = int(yaml_prep_config['hat'])

    def getConfig(self):
        ''' 获取配置
        '''
        config = {}
        config['total_pixels'] = self.total_pixels
        config['gamma'] = self.gamma
        config['sigmod'] = [self.sigmod_center, self.sigmod_zoom]
        config['canny'] = [self.canny_max, self.canny_min]
        config['struct_element_size'] = self.struct_element_size
        config['gauss_blur_size'] = self.gauss_blur_size
        config['hat'] = self.hat
        return config


class TdExtractConfig:
    ''' 连通域提取参数
    '''
    def __init__(self):
        self.delta = 5
        self.min_area = 9
        self.max_area = 500
        self.variation = 0.25
        self.channels = ['Gray']
        self.direction = 1
        self.filter_params = None

    def setConfig(self, yaml_config):
        ''' 设置参数
        '''
        yaml_mser_config = yaml_config['extract']
        self.delta = int(yaml_mser_config['delta'])
        self.channels = yaml_mser_config['channels']
        self.min_area = int(yaml_mser_config['area_lim'][0])
        self.max_area = int(yaml_mser_config['area_lim'][1])
        self.variation = float(yaml_mser_config['variation'])
        self.direction = int(yaml_mser_config['direction'])

        # 基本过滤器参数
        filter_params = {}
        yaml_filter_config = yaml_mser_config['filter_params']
        flag = TdFilterCheckType.AREA.value if "area" in yaml_filter_config['flag'] else 0
        flag += TdFilterCheckType.WIDTH.value if "width" in yaml_filter_config['flag'] else 0
        flag += TdFilterCheckType.HEIGHT.value if "height" in yaml_filter_config['flag'] else 0
        flag += TdFilterCheckType.PERIMETER.value if "perimeter" in yaml_filter_config['flag'] else 0
        flag += TdFilterCheckType.ASPECTRATIO.value if "aspect_ratio" in yaml_filter_config['flag'] else 0
        flag += TdFilterCheckType.OCCUPIEDRATIO.value if "occupied_ratio" in yaml_filter_config['flag'] else 0
        flag += TdFilterCheckType.COMPACTNESS.value if "compactness" in yaml_filter_config['flag'] else 0
        flag += TdFilterCheckType.SWT.value if "swt" in yaml_filter_config['flag'] else 0
        filter_params['flag'] = flag
        filter_params['area_lim'] = int(yaml_filter_config['area_lim'])
        filter_params['perimeter_lim'] = [int(yaml_filter_config['perimeter_lim'][0]), \
                                          int(yaml_filter_config['perimeter_lim'][1])]
        filter_params['aspect_ratio_lim'] = [float(yaml_filter_config['aspect_ratio_lim'][0]), \
                                             float(yaml_filter_config['aspect_ratio_lim'][1])]
        filter_params['aspect_ratio_gt1'] = yaml_filter_config['aspect_ratio_gt1']
        filter_params['occupation_lim'] = [float(yaml_filter_config['occupation_lim'][0]), \
                                           float(yaml_filter_config['occupation_lim'][1])]
        filter_params['compactness_lim'] = [float(yaml_filter_config['compactness_lim'][0]), \
                                            float(yaml_filter_config['compactness_lim'][1])]
        filter_params['width_lim'] = [int(yaml_filter_config['width_lim'][0]), \
                                      int(yaml_filter_config['width_lim'][1])]
        filter_params['height_lim'] = [int(yaml_filter_config['height_lim'][0]), \
                                       int(yaml_filter_config['height_lim'][1])]
        self.filter_params = filter_params

        # SWT 过滤参数
        filter_swt_params = {}
        yaml_filter_swt_config = yaml_filter_config['filter_swt_params']
        filter_swt_params['total_points'] = int(yaml_filter_swt_config['total_points'])
        filter_swt_params['mode_lim'] = float(yaml_filter_swt_config['mode_lim'])
        filter_swt_params['mean_lim'] = [float(yaml_filter_swt_config['mean_lim'][0]), \
                                         float(yaml_filter_swt_config['mean_lim'][1])]
        filter_swt_params['std_lim'] = [float(yaml_filter_swt_config['std_lim'][0]), \
                                        float(yaml_filter_swt_config['std_lim'][1])]
        self.filter_params['swt_params'] = filter_swt_params

    def getConfig(self):
        ''' 获取配置参数
        '''
        config = {}
        config['delta'] = self.delta
        config['channels'] = self.channels
        config['min_area'] = self.min_area
        config['max_area'] = self.max_area
        config['variation'] = self.variation
        config['direction'] = self.direction
        config['filter_params'] = self.filter_params
        return config


class TdConfig(TdPrepConfig, TdExtractConfig):
    ''' 配置文件类
    '''
    def __init__(self, config_file_path="conf/default.yaml"):
        TdPrepConfig.__init__(self)
        TdExtractConfig.__init__(self)
        self.setConfigFromFile(config_file_path)

    def getPrepConfig(self):
        ''' 获取预处理参数
        '''
        return TdPrepConfig.getConfig(self)

    def getExtractConfig(self):
        ''' 获取连通域提取参数
        '''
        return TdExtractConfig.getConfig(self)

    def setConfigFromFile(self, config_file_path):
        ''' 加载配置文件
        '''
        try:
            config_file = open(config_file_path, "r")
        except IOError:
            print("Cannot open file %s" % config_file_path)
            sys.exit()
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        config_file.close()
        TdPrepConfig.setConfig(self, config)
        TdExtractConfig.setConfig(self, config)
