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
        self.canny_max = 0.9
        self.canny_min = 0.7
        self.gamma = 3.0
        self.struct_element_size = 5
        self.gauss_blur_size = 51
        if yaml_config is not None:
            self.setConfig(yaml_config)

    def setConfig(self, yaml_config):
        self.total_pixels = yaml_config['prep']['total_pixels']
        self.channels = yaml_config['prep']['channels']
        self.gamma = yaml_config['prep']['gamma']
        self.struct_element_size = yaml_config['prep']['struct_element_size']
        self.gauss_blur_size = yaml_config['prep']['gauss_blur_size']
        self.canny_max = yaml_config['prep']['canny'][0]
        self.canny_min = yaml_config['prep']['canny'][1]


    def getConfig(self):
        '''
        获取配置
        '''
        config = {}
        config['total_pixels'] = self.total_pixels
        config['channels'] = self.channels
        config['gamma'] = self.gamma
        config['canny'] = [self.canny_max, self.canny_min]
        config['struct_element_size'] = self.struct_element_size
        config['gauss_blur_size'] = self.gauss_blur_size
        return config


class TdConfig(TdPrepConfig):
    '''
    配置文件类
    '''
    def __init__(self, config_file_path="config/default.yaml"):
        TdPrepConfig.__init__(self)
        self.setConfig(config_file_path)

    def getPrepConfig(self):
        '''
        获取预处理参数
        '''
        return TdPrepConfig.getConfig(self)
    
    def setConfig(self, config_file_path):
        '''
        加载配置文件
        '''
        try:
            config_file = open(config_file_path, "r")
        except IOError:
            print("Cannot open file %s" % config_file_path)
            sys.exit()
        config = yaml.load(config_file, Loader=yaml.FullLoader)
        config_file.close()
        TdPrepConfig.setConfig(self, config)



