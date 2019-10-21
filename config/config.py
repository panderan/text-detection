#!/usr/bin/python

'''
读取配置文件
'''

import sys
import yaml

class TdPrepConfig:
    '''
    预处理参数
    '''
    def __init__(self, yaml_config=None):
        self.total_pixels = 400000
        self.channels = ["Gray"]
        self.gamma = 3.0
        self.struct_element_size = 5
        self.gauss_blur_size = 51

        if yaml_config is not None:
            self.total_pixels = yaml_config['prep']['total_pixels']
            self.channels = yaml_config['prep']['channels']
            self.gamma = yaml_config['prep']['gamma']
            self.struct_element_size = yaml_config['prep']['struct_element_size']
            self.gauss_blur_size = yaml_config['prep']['gauss_blur_size']

    def getConfig(self):
        '''
        获取配置
        '''
        config = {}
        config['total_pixels'] = self.total_pixels
        config['channels'] = self.channels
        config['gamma'] = self.gamma
        config['struct_element_size'] = self.struct_element_size
        config['gauss_blur_size'] = self.gauss_blur_size
        return config


class TdConfig(TdPrepConfig):
    '''
    配置文件类
    '''
    def __init__(self, config_file_path="config/default.yaml"):
        try:
            config_file = open(config_file_path, "r")
        except IOError:
            print("Cannot open file %s" % config_file_path)
            sys.exit()
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        config_file.close()
        TdPrepConfig.__init__(self, config)

    def getPrepConfig(self):
        '''
        获取预处理参数
        '''
        return TdPrepConfig.getConfig(self)
