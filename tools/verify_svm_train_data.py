#!/usr/bin/env python

from text_detection import svm
import cv2, sys, getopt, yaml, os, re
import matplotlib.pyplot as plt

# 解析命令行参数
try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["trainpath=","testpath=","config=","verbose"])
except getopt.GetoptError:
    print("argv error")

training_path = ""
arg_config_file_path = ""
verbose = False

for cmd,arg in opts:
    if cmd in ("-h"):
        print("Help Message") 
        sys.exit(0)
    elif cmd in ("--trainpath"):
        training_path = arg[-1] == '/' and arg or "".join([arg,"/"])
    elif cmd in ("--testpath"):
        testing_path = arg[-1] == '/' and arg or "".join([arg,"/"])
    elif cmd in ("--config"):
        arg_config_file_path = arg
    elif cmd in ("--verbose"):
        verbose = True
    else:
        print("Unknown option")
        sys.exit(1)

# 加载配置文件
try:
    config_file = open(arg_config_file_path, "r")
except:
    print("Cannot open file %s"%config_file)
    sys.exit()

config = yaml.load(config_file, Loader=yaml.FullLoader)
config_file.close()

# SVM
classification = svm.svc()
classification.train(training_path)

classification.kernel = config["svm"]["kernel"]
classification.k_c =    config["svm"]["k_c"]
classification.gamma =  config["svm"]["gamma"]
classification.degree = config["svm"]["degree"]

for root, dirs, files in os.walk(testing_path, topdown=True):
    if root==testing_path:
        for filename in files:
            if re.search('[jpg|png]$', filename):
                label = filename[-5]
                filepath = "".join([root,filename])
                img = cv2.imread(filepath, 0)
                retprd = classification.predict(img)
                if label != retprd or verbose:
                    print("%c-%c | file:%s" %(label,retprd,filename))


