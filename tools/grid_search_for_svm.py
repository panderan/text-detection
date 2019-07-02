from text_detection import svm
import cv2, sys, getopt, yaml, os, re, math
import matplotlib.pyplot as plt


# 解析命令行参数
try:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["path=", "verbose"])
except getopt.GetoptError:
    print("argv error")

training_path = ""
arg_verbose = False
for cmd,arg in opts:
    if cmd in ("-h"):
        print("Help Message")
        sys.exit(0)
    elif cmd in ("--path"):
        training_path = arg[-1] == '/' and arg or "".join([arg,"/"])
    elif cmd in ("--verbose"):
        arg_verbose = True
    else:
        print("Unknown option")
        sys.exit(1)

tuned_parameters1 = [{'kernel':['rbf'], 
                     'gamma':[1, 1e-1,1e-2,1e-3,1e-4,1e-5,1e-6,1e-7], 
                     'C':[1,5,6,7,8,9,10,20,30,40,50]}]

tuned_parameters2 = [{'kernel':['poly'], 
                      'gamma':['scale'],  
                      'degree':[a for a in range(3,30,1)]}]

classification = svm.svc()
classification.grid_search(training_path, tuned_parameters1, ["accuracy"], arg_verbose)
