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
        self.prep_configs = {
            'total_pixels': 0,          # 总像素量
            'canny_max': 0.0,           # canny 上限
            'canny_min': 0.0,           # canny 下限
            'gamma': 0.0,               # gamma 值
            'sobel': False,             # 是否过滤掉水平边缘
            'sigmod_center': 0.0,       # sigmod 中心点 [0.0, 1.0]
            'sigmod_zoom': 0,           # sigmod 缩放倍率
            'struct_element_size': 0,   # 结构元素大小 RECT
            'gauss_blur_size': 0,       # 高斯模糊大小
            'hat': 0                    # 顶底冒运算
        }
        if yaml_config is not None:
            self.setConfig(yaml_config)

    def setConfig(self, configs):
        ''' 设置配置文件
        '''
        yaml_data = configs['prep']
        TdPrepConfig.setConfigItem(self, 'total_pixels', int(yaml_data.get('total_pixels', 0)))
        TdPrepConfig.setConfigItem(self, 'gamma', float(yaml_data.get('gamma', 0.0)))
        TdPrepConfig.setConfigItem(self, 'struct_element_size', int(yaml_data.get('struct_element_size', 0)))
        TdPrepConfig.setConfigItem(self, 'gauss_blur_size', int(yaml_data.get('gauss_blur_size', 0)))
        TdPrepConfig.setConfigItem(self, 'sigmod_center', float(yaml_data.get('sigmod', [0, 0])[0]))
        TdPrepConfig.setConfigItem(self, 'sigmod_zoom', float(yaml_data.get('sigmod', [0, 0])[1]))
        TdPrepConfig.setConfigItem(self, 'canny_max', float(yaml_data.get('canny', [0, 0])[0]))
        TdPrepConfig.setConfigItem(self, 'canny_min', float(yaml_data.get('canny', [0, 0])[1]))
        TdPrepConfig.setConfigItem(self, 'sobel', yaml_data.get('sobel', False))
        TdPrepConfig.setConfigItem(self, 'hat', int(yaml_data.get('hat', 0)))

    def setConfigItem(self, key, value):
        ''' 设置单个参数
        '''
        if self.prep_configs.get(key, None) is not None:
            self.prep_configs[key] = value
            return True
        return False

    def getConfig(self):
        ''' 获取配置
        '''
        return self.prep_configs


class TdExtractConfig:
    ''' 连通域提取参数
    '''
    def __init__(self):
        self.ext_configs = {
            'delta': 0,
            'channels': ['Gray'],
            'min_area': 0,
            'max_area': 0,
            'variation': 0.0,
            'direction': 0,
            'debug': False,
            'show_verbose': False
        }

    def setConfig(self, configs):
        ''' 设置参数
        '''
        yaml_data = configs['extract']
        TdExtractConfig.setConfigItem(self, 'delta', int(yaml_data.get('delta', 0)))
        TdExtractConfig.setConfigItem(self, 'channels', yaml_data.get('channels', ["Gray"]))
        TdExtractConfig.setConfigItem(self, 'min_area', int(yaml_data.get('area_lim', [0, 0])[0]))
        TdExtractConfig.setConfigItem(self, 'max_area', int(yaml_data.get('area_lim', [0, 0])[1]))
        TdExtractConfig.setConfigItem(self, 'variation', float(yaml_data.get('variation', 0.0)))
        TdExtractConfig.setConfigItem(self, 'direction', int(yaml_data.get('direction', 0)))
        TdExtractConfig.setConfigItem(self, 'debug', False)
        TdExtractConfig.setConfigItem(self, 'show_verbose', False)

    def setConfigItem(self, key, value):
        ''' 设置单个参数
        '''
        if self.ext_configs.get(key, None) is not None:
            self.ext_configs[key] = value
            return True
        return False

    def getConfig(self):
        ''' 获取配置参数
        '''
        return self.ext_configs


class TdFilterConfig:
    ''' 过滤器参数
    '''
    def __init__(self):
        self.flt_configs = {
            'default': {
                'flag': 0,
                'area_lim': 0,
                'width_lim': [0, 0],
                'height_lim': [0, 0],
                'perimeter_lim': [0, 0],
                'aspect_ratio_lim': [0, 0],
                'asecpt_ratio_gt1': True,
                'occupation_lim': [0, 0],
                'compactness_lim': [0, 0],
                'swt': {
                    'total_points': 0,
                    'mode_lim': 0,
                    'mean_lim': [0, 0],
                    'std_lim': [0, 0]
                }
            }
        }

    def setConfig(self, configs):
        ''' 设置过滤器配置
        '''
        for fltname in configs['filters'].keys():
            yaml_data = configs['filters'][fltname]
            self.addNewFilter(fltname)
            flag = TdFilterCheckType.AREA.value if "area" in yaml_data.get('flag', 0) else 0
            flag += TdFilterCheckType.WIDTH.value if "width" in yaml_data.get('flag', 0) else 0
            flag += TdFilterCheckType.HEIGHT.value if "height" in yaml_data.get('flag', 0) else 0
            flag += TdFilterCheckType.PERIMETER.value if "perimeter" in yaml_data.get('flag', 0) else 0
            flag += TdFilterCheckType.ASPECTRATIO.value if "aspect_ratio" in yaml_data.get('flag', 0) else 0
            flag += TdFilterCheckType.OCCUPIEDRATIO.value if "occupied_ratio" in yaml_data.get('flag', 0) else 0
            flag += TdFilterCheckType.COMPACTNESS.value if "compactness" in yaml_data.get('flag', 0) else 0
            flag += TdFilterCheckType.SWT.value if "swt" in yaml_data.get('flag', 0) else 0
            TdFilterConfig.setConfigItem(self, fltname, 'flag', flag)
            TdFilterConfig.setConfigItem(self, fltname, 'area_lim', int(yaml_data.get('area_lim', 0)))
            TdFilterConfig.setConfigItem(self, fltname, 'perimeter_lim', [int(yaml_data.get('perimeter_lim', [0, 0])[0]), int(yaml_data.get('perimeter_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, 'aspect_ratio_lim', [float(yaml_data.get('aspect_ratio_lim', [0, 0])[0]), float(yaml_data.get('aspect_ratio_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, 'occupation_lim', [float(yaml_data.get('occupation_lim', [0, 0])[0]), float(yaml_data.get('occupation_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, 'compactness_lim', [float(yaml_data.get('compactness_lim', [0, 0])[0]), float(yaml_data.get('compactness_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, 'width_lim', [int(yaml_data.get('width_lim', [0, 0])[0]), int(yaml_data.get('width_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, 'height_lim', [int(yaml_data.get('height_lim', [0, 0])[0]), int(yaml_data.get('height_lim', [0, 0])[1])])
            TdFilterConfig.setConfigItem(self, fltname, 'aspect_ratio_gt1', yaml_data.get('aspect_ratio_gt1', True))

            # SWT 过滤参数
            yaml_swt_data = yaml_data.get('swt', None)
            if yaml_swt_data is not None:
                swt_config = {}
                yaml_swt_data = yaml_data['swt']
                swt_config['total_points'] = int(yaml_swt_data.get('total_points', 0))
                swt_config['mode_lim'] = float(yaml_swt_data.get('mode_lim', 0))
                swt_config['mean_lim'] = [float(yaml_swt_data.get('mean_lim', [0, 0])[0]), float(yaml_swt_data.get('mean_lim', [0, 0])[1])]
                swt_config['std_lim'] = [float(yaml_swt_data.get('std_lim', [0, 0])[0]), float(yaml_swt_data.get('std_lim', [0, 0])[1])]
                TdFilterConfig.setConfigItem(self, fltname, 'swt', swt_config)

    def setConfigItem(self, fltname, key, value):
        ''' 设置单个参数
        '''
        if self.flt_configs.get(fltname, None) is not None:
            sub_config = self.flt_configs[fltname]
            if sub_config.get(key, None) is not None:
                sub_config[key] = value
            return True
        return False

    def addNewFilter(self, fltname):
        ''' 新增 filter
        '''
        newconf = {
            'flag': 0,
            'area_lim': 0,
            'width_lim': [0, 0],
            'height_lim': [0, 0],
            'perimeter_lim': [0, 0],
            'aspect_ratio_lim': [0, 0],
            'aspect_ratio_gt1': True,
            'occupation_lim': [0, 0],
            'compactness_lim': [0, 0],
            'swt': {
                'total_points': 0,
                'mode_lim': 0,
                'mean_lim': [0, 0],
                'std_lim': [0, 0]
            }
        }
        self.flt_configs[fltname] = newconf

    def getConfig(self, keystr):
        ''' 获取过滤器配置
        '''
        return self.flt_configs.get(keystr, None)


class TdMergeTLConfig:
    ''' 文本行合并参数
    '''
    def __init__(self):
        self.meg_configs = {
            'combined_area_size_lim': 0,
            'combined_aspect_ratio_lim': [0.0, 0.0],
            'overlap_ratio': 0.25,
            'distance': 0.0,
            'strategy': "horizon",
            'show_verbose': False
        }

    def setConfig(self, configs):
        ''' 设置配置
        '''
        yaml_data = configs['mergetl']
        TdMergeTLConfig.setConfigItem(self, 'combined_area_size_lim', int(yaml_data.get('combined_area_size_lim', 0)))
        TdMergeTLConfig.setConfigItem(self, 'combined_aspect_ratio_lim', [float(v) for v in yaml_data.get('combined_aspect_ratio_lim', [0.0, 0.0])])
        TdMergeTLConfig.setConfigItem(self, 'overlap_ratio', float(yaml_data.get('overlap_ratio', 0)))
        TdMergeTLConfig.setConfigItem(self, 'distance', float(yaml_data.get('distance', 0)))
        TdMergeTLConfig.setConfigItem(self, 'strategy', yaml_data.get('strategy', "horizon"))

    def setConfigItem(self, key, value):
        ''' 设置单个参数
        '''
        if self.meg_configs.get(key, None) is not None:
            self.meg_configs[key] = value
            return True
        return False

    def getConfig(self):
        ''' 获取配置
        '''
        return self.meg_configs


class TdConfig(TdPrepConfig, TdExtractConfig, TdMergeTLConfig, TdFilterConfig):
    ''' 配置文件类
    '''
    def __init__(self, config_file_path="conf/default.yaml"):
        TdPrepConfig.__init__(self)
        TdExtractConfig.__init__(self)
        TdMergeTLConfig.__init__(self)
        TdFilterConfig.__init__(self)
        self.setConfigFromFile(config_file_path)

    def getPrepConfig(self):
        ''' 获取预处理参数
        '''
        return TdPrepConfig.getConfig(self)

    def getExtractConfig(self):
        ''' 获取连通域提取参数
        '''
        return TdExtractConfig.getConfig(self)

    def getMergeTLConfig(self):
        ''' 获取文本行合并参数
        '''
        return TdMergeTLConfig.getConfig(self)

    def getFilterConfig(self, keystr):
        ''' 获取过滤器参数
        '''
        return TdFilterConfig.getConfig(self, keystr)

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
        TdMergeTLConfig.setConfig(self, config)
        TdFilterConfig.setConfig(self, config)
