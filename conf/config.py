#!/usr/bin/python

''' 读取配置文件
'''

import sys
import yaml

class TdPrepConfig:
    ''' 预处理参数
    '''
    def __init__(self, yaml_config=None):
        self.total_pixels = 400000
        self.canny_max = 0.9
        self.canny_min = 0.7
        self.gamma = 3.0
        self.struct_element_size = 5
        self.gauss_blur_size = 51
        if yaml_config is not None:
            self.setConfig(yaml_config)

    def setConfig(self, yaml_config):
        ''' 设置配置文件
        '''
        self.total_pixels = int(yaml_config['prep']['total_pixels'])
        self.gamma = float(yaml_config['prep']['gamma'])
        self.struct_element_size = int(yaml_config['prep']['struct_element_size'])
        self.gauss_blur_size = int(yaml_config['prep']['gauss_blur_size'])
        self.canny_max = float(yaml_config['prep']['canny'][0])
        self.canny_min = float(yaml_config['prep']['canny'][1])

    def getConfig(self):
        ''' 获取配置
        '''
        config = {}
        config['total_pixels'] = self.total_pixels
        config['gamma'] = self.gamma
        config['canny'] = [self.canny_max, self.canny_min]
        config['struct_element_size'] = self.struct_element_size
        config['gauss_blur_size'] = self.gauss_blur_size
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
        self.filter_params = None
        self.filter_swt_params = None

    def setConfig(self, yaml_config):
        ''' 设置参数
        '''
        self.delta = int(yaml_config['extract']['delta'])
        self.channels = yaml_config['extract']['channels']
        self.min_area = int(yaml_config['extract']['area_lim'][0])
        self.max_area = int(yaml_config['extract']['area_lim'][1])
        self.variation = float(yaml_config['extract']['variation'])

        # 基本过滤器参数
        filter_params = {}
        filter_params['flag'] = int(yaml_config['extract']['filter_params']['flag'])
        filter_params['area_lim'] = int(yaml_config['extract']['filter_params']['area_lim'])
        filter_params['perimeter_lim'] = int(yaml_config['extract']['filter_params']['perimeter_lim'])
        filter_params['aspect_ratio_lim'] = [float(yaml_config['extract']['filter_params']['aspect_ratio_lim'][0]), \
                                             float(yaml_config['extract']['filter_params']['aspect_ratio_lim'][1])]
        filter_params['aspect_ratio_gt1'] = yaml_config['extract']['filter_params']['aspect_ratio_gt1']
        filter_params['occupation_lim'] = [float(yaml_config['extract']['filter_params']['occupation_lim'][0]), \
                                           float(yaml_config['extract']['filter_params']['occupation_lim'][1])]
        filter_params['compactness_lim'] = [float(yaml_config['extract']['filter_params']['compactness_lim'][0]), \
                                            float(yaml_config['extract']['filter_params']['compactness_lim'][1])]
        filter_params['width_lim'] = [int(yaml_config['extract']['filter_params']['width_lim'][0]), \
                                      int(yaml_config['extract']['filter_params']['width_lim'][1])]
        filter_params['height_lim'] = [int(yaml_config['extract']['filter_params']['height_lim'][0]), \
                                       int(yaml_config['extract']['filter_params']['height_lim'][1])]
        self.filter_params = filter_params

        # SWT 过滤参数
        filter_swt_params = {}
        filter_swt_params['total_points'] = int(yaml_config['extract']['filter_swt_params']['total_points'])
        filter_swt_params['mode_lim'] = float(yaml_config['extract']['filter_swt_params']['mode_lim'])
        filter_swt_params['mean_lim'] = [float(yaml_config['extract']['filter_swt_params']['mean_lim'][0]), \
                                         float(yaml_config['extract']['filter_swt_params']['mean_lim'][1])]
        filter_swt_params['std_lim'] = [float(yaml_config['extract']['filter_swt_params']['std_lim'][0]), \
                                        float(yaml_config['extract']['filter_swt_params']['std_lim'][1])]
        self.filter_swt_params = filter_swt_params

    def getConfig(self):
        ''' 获取配置参数
        '''
        config = {}
        config['delta'] = self.delta
        config['channels'] = self.channels
        config['min_area'] = self.min_area
        config['max_area'] = self.max_area
        config['variation'] = self.variation
        config['filter_params'] = self.filter_params
        config['filter_swt_params'] = self.filter_swt_params
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
