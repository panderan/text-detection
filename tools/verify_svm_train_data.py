#!/usr/bin/env python

from text_detection import svm
import cv2, sys, getopt, yaml, os, re
import matplotlib.pyplot as plt

# 解析命令行参数
try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["path="])
except getopt.GetoptError:
    print("argv error")

training_path = ""
for cmd,arg in opts:
    if cmd in ("-h"):
        print("Help Message")
        sys.exit(0)
    elif cmd in ("--path"):
        training_path = arg[-1] == '/' and arg or "".join([arg,"/"])
    else:
        print("Unknown option")
        sys.exit(1)

classification = svm.svc()
classification.train(training_path)

for root, dirs, files in os.walk(training_path, topdown=True):
    if root==training_path:
        for filename in files:
            if re.search('[jpg|png]$', filename):
                label = filename[-5]
                filepath = "".join([root,filename])
                img = cv2.imread(filepath, 0)
                retprd = classification.predict(img)
                if label != retprd:
                    print("%c-%c | file:%s" %(label,retprd,filename))


