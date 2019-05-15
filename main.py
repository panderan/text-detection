#!/usr/bin/env python

## @file main.py
# 将一幅输入的图像中的候选区域分别保存为图片
#   
# @author panderan@163.com 
#

from text_detection import mser, filter, morph, contours, svm, regions, evaluate
import matplotlib.pyplot as plt
import cv2
import sys
import getopt

save_region = False
save_regions_path = ""
save_mask=False
save_mask_path = ""
enable_svm = False
enable_eval = False
ground_truth_img_path = ""

enable_debug_mser=False
enable_debug_morph=False
enable_debug_contours=False
enable_debug_contours_verbose=False

def usage():
    print("Help message")

try:
    opts, args = getopt.getopt(sys.argv[1:], "i:", ["svm","save-regions=","eval=","save-mask=","debug=","help"])
except getopt.GetoptError:
    print("argv error")

for cmd,arg in opts:
    if cmd in ("-i"):
        image_path = arg
    elif cmd in ("--save-regions"):
        save_regions_path = arg
        save_region = True 
    elif cmd in ("--save-mask"):
        save_mask_path = arg
        save_mask = True
    elif cmd in ("--svm"):
        enable_svm = True
    elif cmd in ("--eval"):
        enable_eval = True
        ground_truth_img_path = arg
    elif cmd in ("--debug"):
        ss = arg.split(',')
        if "mser" in ss:
            enable_debug_mser=True
        if "morph" in ss:
            enable_debug_morph = True
        if "contours" in ss:
            enable_debug_contours = True
        if "contours-verbose" in ss:
            enable_debug_contours_verbose = True
    else:
        usage()
        sys.exit()

print("Iput Image: %s" % image_path)

# 创建 MSER 实例和几何过滤实例，提取 MSER 选区
msr = mser.mser_cls(image_path)
flt = filter.mser_filter400k()
binaries = msr.extraction_in_all_channel_with_labels(flt = flt)


# 对由候选区组成的二值图像进行形态学处理
mph = morph.morph()
binaries = mph.morph_operation(binaries, debug=enable_debug_morph)


# 创建选区处理实例，并从二值图像中提起候选区域分别保存为图片
ctr = contours.tdcontours(binaries, image_path.split('/')[-1][0:-4], save_regions_path)
ctr.aggreate_contours_using_boxes(debug=enable_debug_contours, debug_verbose=enable_debug_contours_verbose)

if save_region:
    ctr.save_each_contours_using_boxes(msr.gray_img, True)
    sys.exit()

# SVM 分类
text_regions_binaries = ctr.binaries.copy()
if enable_svm:
    classification = svm.svc()
    classification.train("IDCards/Rear/Training")
    text_regions_binaries = classification.filter_regions(msr.gray_img, ctr.binaries)

# 评估结果
if enable_eval:
    e = evaluate.evaluate()
    gt_img = cv2.imread(ground_truth_img_path, 0)
    _, gt_img = cv2.threshold(gt_img, 128, 255, cv2.THRESH_BINARY)
    gt_img = cv2.resize(gt_img, (ctr.binaries.shape[1],ctr.binaries.shape[0]))
    precision = e.precision(ctr.boxes, gt_img)
    recall = e.recall(ctr.boxes, gt_img)
    print("\nResult:")
    print("Precision: %.3f\nRecall:%.3f" %(precision, recall))

# 保存 mask
if save_mask:
    cv2.imwrite(save_mask_path+"/"+image_path.split('/')[-1], ctr.binaries)

# 标记最终选区
ret_img = regions.regions.label_image_with_box(msr.gray_img, ctr.boxes)
plt.figure(figsize=(10,8))
plt.imshow(ret_img, "gray")
plt.show()

