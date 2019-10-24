#!/usr/bin/env python

'''
text-detection 命令行程序(CLI)
'''

import sys
import getopt
import cv2
import matplotlib.pyplot as plt
from gui.text_detection.preprocessing import TdPreprocessing
from conf.config import TdConfig

def usage():
    '''
    显示帮助信息
    '''
    print("Help message")

class cli:
    '''
    text-detection 命令行程序(CLI)
    '''
    def __init__(self):
        self.image_path = None
        self.image_name = None
        self.config_file_path = None
        self.preprocessing = TdPreprocessing()
        self.config = TdConfig()

    def run(self):
        '''
        运行命令
        '''
        # 解析命令行参数
        self.parseArgs()

        # 加载配置
        self.config.setConfig(self.config_file_path)
        # 读取输入
        imput_image = cv2.imread(self.image_path)

        # 预处理
        self.preprocessing.setImage(imput_image)
        preped_images_dict = self.preprocessing.doPreprocessing("Blue Channel", \
                                                self.config.getPrepConfig())
        plt.imshow(preped_images_dict["Result"], "gray")
        plt.show()

    def parseArgs(self):
        '''
        解析命令行参数
        '''
        try:
            opts, _ = getopt.getopt(sys.argv[1:], "i:", \
                            ["svm=", "save-regions=", "eval=", "save-mask=", \
                            "debug=", "disable-show", "config=", "cProfile=", \
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
            else:
                usage()
                sys.exit(1)




if __name__ == '__main__':
    app = cli()
    app.run()
