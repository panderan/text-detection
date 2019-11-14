#!/usr/bin/env python

''' text-detection 命令行程序(CLI)
'''

import logging
import sys
import getopt
from enum import Enum
import cv2
import matplotlib.pyplot as plt
from gui.text_detection.preprocessing import TdPreprocessing
from gui.text_detection.extract_connect_domain import TdExtractConnectDomain
from gui.text_detection.region_filter import TdFilter
from gui.text_detection.morph_ops import TdMorphOperator
from gui.text_detection.merging_textline import TdMergingTextLine, debugGenerateElectionImage
from conf.config import TdConfig


logging.basicConfig(level=logging.INFO, \
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', \
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger(__name__)


def usage():
    ''' 显示帮助信息
    '''
    print("Help message")


class CliShowOptions(Enum):
    ''' 显示选项
    '''
    SHOW_NONE = 0
    SHOW_PREP = 1
    SHOW_EXTRACT = 2
    SHOW_MORPH = 4
    SHOW_MERGE = 8
    SHOW_FEATURE = 16
    SHOW_RESULT = 32


class Cli:
    ''' text-detection 命令行程序(CLI)
    '''
    def __init__(self):
        self.image_path = None
        self.image_name = None
        self.config_file_path = None
        self.preprocessing = TdPreprocessing()
        self.extracter = TdExtractConnectDomain()
        self.filter = TdFilter()
        self.merger = TdMergingTextLine()

        self.config = TdConfig()
        self.morpher = TdMorphOperator()
        self.show_opts = CliShowOptions.SHOW_RESULT.value

    def run(self):
        '''
        运行命令
        '''
        # 解析命令行参数
        self.parseArgs()

        # 加载配置
        self.config.setConfigFromFile(self.config_file_path)

        # 读取输入
        imput_image = cv2.imread(self.image_path)

        # 预处理
        self.preprocessing.setConfig(self.config.getPrepConfig())
        self.preprocessing.setImage(imput_image)
        if self.show_opts & CliShowOptions.SHOW_PREP.value:
            plt.imshow(self.preprocessing.blue_channel_preped, "gray")
            plt.show()

        # 连通域提取
        self.extracter.setConfig(self.config.getExtractConfig())
        tmp_filter = self.filter.setConfig(self.config.getExtractConfig()["filter_params"])
        _, binarized = self.extracter.extract_with_labels({"name":"Blue", "image":self.preprocessing.blue_channel_preped}, tmp_filter)
        if self.show_opts & CliShowOptions.SHOW_EXTRACT.value:
            plt.imshow(binarized, "gray")
            plt.show()

        # 形态学处理
        regions = self.morpher.morph_operation(binarized)
        if self.show_opts & CliShowOptions.SHOW_MORPH.value:
            verbose_image = self.morpher.getMaskImage(binarized, regions)
            plt.imshow(verbose_image, "gray")
            plt.show()

        # 文本行合并
        self.merger.debug_data['shape'] = binarized.shape
        self.merger.debug_enable = True
        self.merger.mergeTextLine(regions)
        image = debugGenerateElectionImage(self.merger.debug_data, 0)
        plt.imshow(image)
        plt.show()

    def parseArgs(self):
        '''
        解析命令行参数
        '''
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "i:", \
                            ["svm=", "save-regions=", "eval=", "save-mask=", \
                            "debug=", "show=", "config=", "cProfile=", \
                            "ocolor=", "ogray=", "color", "gray", "prep", "help"])
        except getopt.GetoptError:
            print("argv error")
            sys.exit(1)

        for cmd, arg in opts:
            if cmd in "-i":
                self.image_path = arg
                self.image_name = self.image_path.split('/')[-1][0:-4]
            elif cmd in "--config":
                self.config_file_path = arg
            elif cmd in "--show":
                options = arg.split(',')
                if "prep" in options:
                    self.show_opts |= CliShowOptions.SHOW_PREP.value
                if "extract" in options:
                    self.show_opts |= CliShowOptions.SHOW_EXTRACT.value
                if "merge" in options:
                    self.show_opts |= CliShowOptions.SHOW_MERGE.value
                if "feature" in options:
                    self.show_opts |= CliShowOptions.SHOW_FEATURE.value
                if "none" in options:
                    self.show_opts = CliShowOptions.SHOW_NONE.value
            else:
                usage()
                sys.exit(1)


if __name__ == '__main__':
    app = Cli()
    app.run()
