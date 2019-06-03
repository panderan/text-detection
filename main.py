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
import yaml

save_region = False
save_regions_path = ""
save_mask=False
save_mask_path = ""
enable_svm = False
training_path = ""
enable_eval = False
ground_truth_img_path = ""
config_file_path = "config/default.yaml"

enable_debug_mser=False
enable_debug_morph=False
enable_debug_contours=False
enable_debug_contours_verbose=False
enable_debug_svm=False
is_show_result = True


def usage():
    print("Help message")


try:
    opts, args = getopt.getopt(sys.argv[1:], "i:", ["svm=","save-regions=","eval=","save-mask=","debug=","disable-show","config=","help"])
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
        training_path = arg
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
        if "svm" in ss:
            enable_debug_svm = True
    elif cmd in ("--disable-show"):
        is_show_result = False
    elif cmd in ("--config"):
        config_file_path = arg
    else:
        usage()
        sys.exit()


print("Iput Image: %s" % image_path)
imput_image = cv2.imread(image_path)

# 加载配置文件
try:
    config_file = open(config_file_path, "r")
except:
    print("Cannot open file %s"%config_file)
    sys.exit()

config = yaml.load(config_file, Loader=yaml.FullLoader)
config_file.close()


# 创建 MSER 实例和几何过滤实例，提取 MSER 选区
msr = mser.mser_cls()
msr.min_area     = config['mser']['min_area']
msr.max_area     = config['mser']['max_area']
msr.variation    = config['mser']['variation']
msr.total_pixels = config['mser']['total_pixels']

msr_flt = filter.mser_filter()
msr_flt.perimeter_lim    = config['mser_filter']['perimeter_lim']
msr_flt.aspect_ratio_lim = config['mser_filter']['aspect_ratio_lim']
msr_flt.occupation_lim   = config['mser_filter']['occupation_lim']
msr_flt.compactness_lim  = config['mser_filter']['compactness_lim']

binaries = msr.extraction_in_all_channel_with_labels(imput_image, flt = msr_flt)


# 对由候选区组成的二值图像进行形态学处理
mph = morph.morph()
mph.k_erode   = cv2.getStructuringElement(cv2.MORPH_RECT, (config['morph']['k_erode'],config['morph']['k_erode']))
mph.k_dilate  = cv2.getStructuringElement(cv2.MORPH_RECT, (config['morph']['k_dilate'],config['morph']['k_dilate']))
mph.k_opening = cv2.getStructuringElement(cv2.MORPH_RECT, (config['morph']['k_opening'],config['morph']['k_opening']))
mph.k_closing = cv2.getStructuringElement(cv2.MORPH_RECT, (config['morph']['k_closing'],config['morph']['k_closing']))

mph_flt = None
if config['morph_filter']['enable'] == True:
    mph_flt = filter.filter()
    mph_flt.area_lim = config['morph_filter']['area_lim']
    mph_flt.aspect_lim = config['morph_filter']['aspect_lim']
binaries = mph.morph_operation(binaries, flt=mph_flt, debug=enable_debug_morph)


# 创建选区处理实例，并从二值图像中提起候选区域分别保存为图片
ctr = contours.tdcontours(binaries, image_path.split('/')[-1][0:-4], save_regions_path)
ctr.t_of_extreme_area_ratio_for_ab = config['contours']['extreme_area_ratio_for_ab']
ctr.t_of_overlap_ratio = config['contours']['overlap_ratio']
ctr.t_of_area_size = config['contours']['area_size']
ctr.t_of_ar_of_direction_type = config['contours']['ar_of_direction_type']
ctr.t_of_distance = config['contours']['distance']

ctr.aggreate_contours_using_boxes(debug=enable_debug_contours, debug_verbose=enable_debug_contours_verbose)
if config['contours_filter']['enable'] == True:
    ctr_flt = filter.filter()
    ctr_flt.area_lim = config['contours_filter']['area_lim']
    ctr_flt.aspect_lim = config['contours_filter']['aspect_lim']
    ctr.flesh_binaries_using_filtered_boxes(ctr_flt)

# 生成训练数据
if save_region:
    ctr.save_each_contours_using_boxes(msr.gray_img, True)
    sys.exit()


# SVM 检测分类
text_regions_binaries = ctr.binaries.copy()
if enable_svm:
    classification = svm.svc()
    classification.train(training_path)
    ctr.boxes = classification.filter_regions(msr.gray_img, ctr.boxes, enable_debug_svm)
    ctr.flesh_binaries_using_boxes()


# 计算 f-measure 评估结果
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
    cv2.imwrite(save_mask_path+"/mask-"+image_path.split('/')[-1], ctr.binaries)
    cv2.imwrite(save_mask_path+"/orig-"+image_path.split('/')[-1], msr.gray_img)


# 标记最终选区
if is_show_result:
    ret_img = regions.regions.label_image_with_box(msr.gray_img, ctr.boxes)
    plt.figure(figsize=(10,8))
    plt.imshow(ret_img, "gray")
    plt.show()

