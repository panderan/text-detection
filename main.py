#!/usr/bin/env python

## @file main.py
# 将一幅输入的图像中的候选区域分别保存为图片
#   
# @author panderan@163.com 
#

from text_detection import mser, filter, morph, contours, svm, regions, evaluate
import matplotlib.pyplot as plt
import cv2, sys, getopt, yaml
import numpy as np
import cProfile 


# 命令行参数变量
arg_save_region = False
arg_save_regions_path = ""
arg_save_mask=False
arg_save_mask_path = ""
arg_enable_svm = False
arg_training_path = ""
arg_enable_eval = False
arg_ground_truth_img_path = ""
arg_config_file_path = "config/default.yaml"
arg_is_show_result = True
arg_color = False
arg_ocolor = ""
arg_gray = True 
arg_ogray = ""
arg_prep = False

arg_enable_debug_mser=False
arg_enable_debug_morph=False
arg_enable_debug_contours=False
arg_enable_debug_contours_filter=False
arg_enable_debug_contours_verbose=False
arg_enable_debug_svm=False

arg_profile_mser=False
arg_profile_morph=False
arg_profile_contours=False
arg_profile_svm=False

cfg_mser_target_channels=mser.EXTRACT_NONE

# 帮助信息
def usage():
    print("Help message")


# 解析命令行参数
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:", \
                    ["svm=","save-regions=","eval=","save-mask=", \
                    "debug=","disable-show","config=","cProfile=", \
                    "ocolor=","ogray=","color", "gray", "prep","help"])
except getopt.GetoptError:
    print("argv error")

for cmd,arg in opts:
    if cmd in ("-i"):
        image_path = arg
        image_name = image_path.split('/')[-1][0:-4]
    elif cmd in ("--save-regions"):
        arg_save_region = True 
        arg_save_regions_path = arg[-1] == '/' and arg or "".join([arg,"/"])
    elif cmd in ("--save-mask"):
        arg_save_mask_path = arg
        arg_save_mask = True
    elif cmd in ("--svm"):
        arg_enable_svm = True
        arg_training_path = arg
    elif cmd in ("--eval"):
        arg_enable_eval = True
        arg_ground_truth_img_path = arg
    elif cmd in ("--debug"):
        ss = arg.split(',')
        if "mser" in ss:
            arg_enable_debug_mser=True
        if "morph" in ss:
            arg_enable_debug_morph = True
        if "contours" in ss:
            arg_enable_debug_contours = True
        if "contours-filter" in ss:
            arg_enable_debug_contours_filter = True
        if "contours-verbose" in ss:
            arg_enable_debug_contours_verbose = True
        if "svm" in ss:
            arg_enable_debug_svm = True
    elif cmd in ("--cProfile"):
        ss = arg.split(',')
        if "mser" in ss:
            arg_profile_mser=True
        if "morph" in ss:
            arg_profile_morph = True
        if "contours" in ss:
            arg_profile_contours = True
        if "svm" in ss:
            arg_profile_svm = True
    elif cmd in ("--disable-show"):
        arg_is_show_result = False
    elif cmd in ("--ocolor"):
        arg_ocolor = arg 
        arg_color = True
    elif cmd in ("--ogray"):
        arg_ogray = arg 
        arg_gray = True 
    elif cmd in ("--color"):
        arg_color = True
    elif cmd in ("--gray"):
        arg_gray = True 
    elif cmd in ("--prep"):
        arg_prep = True 
    elif cmd in ("--config"):
        arg_config_file_path = arg
    else:
        usage()
        sys.exit()


# 读取输入图像文件
print("Iput Image: %s" % image_path)
imput_image = cv2.imread(image_path)


# 加载配置文件
try:
    config_file = open(arg_config_file_path, "r")
except:
    print("Cannot open file %s"%config_file)
    sys.exit()

config = yaml.load(config_file, Loader=yaml.FullLoader)
config_file.close()


# 创建 MSER 实例和简单特征检测实例，提取 MSER 选区
msr = mser.mser_cls()
msr.min_area     = config['mser']['min_area']
msr.max_area     = config['mser']['max_area']
msr.variation    = config['mser']['variation']
msr.gamma        = config['mser']['gamma']
msr.total_pixels = config['mser']['total_pixels']
for item in config['mser']['channels']:
    if item == "Green":
        cfg_mser_target_channels += mser.EXTRACT_GREEN
    if item == "Red":
        cfg_mser_target_channels += mser.EXTRACT_RED
    if item == "Blue":
        cfg_mser_target_channels += mser.EXTRACT_BLUE
    if item == "Gray":
        cfg_mser_target_channels += mser.EXTRACT_GRAY

msr_flt = filter.basicFilter()
msr_flt.perimeter_lim    = config['mser_filter']['perimeter_lim']
msr_flt.aspect_ratio_lim = config['mser_filter']['aspect_ratio_lim']
msr_flt.aspect_ratio_gt1 = config['mser_filter']['aspect_ratio_gt1']
msr_flt.occupation_lim   = config['mser_filter']['occupation_lim']
msr_flt.compactness_lim  = config['mser_filter']['compactness_lim']
msr_flt.width_lim   = config['mser_filter']['width_lim']
msr_flt.height_lim  = config['mser_filter']['height_lim']

if arg_profile_mser:
    cProfile.run('binaries = msr.extraction_in_all_channel_with_labels(imput_image, \
                                    flt = msr_flt, debug=arg_enable_debug_mser)')
else:
    binaries = msr.extraction_in_channels_with_labels(imput_image, channel=cfg_mser_target_channels, \
                                    flt = msr_flt, debug=arg_enable_debug_mser)


# 对由候选区组成的二值图像进行形态学处理
mph = morph.morph()
mph.k_erode   = cv2.getStructuringElement(cv2.MORPH_RECT, (config['morph']['k_erode'],config['morph']['k_erode']))
mph.k_dilate  = cv2.getStructuringElement(cv2.MORPH_RECT, (config['morph']['k_dilate'],config['morph']['k_dilate']))
mph.k_opening = cv2.getStructuringElement(cv2.MORPH_RECT, (config['morph']['k_opening'],config['morph']['k_opening']))
mph.k_closing = cv2.getStructuringElement(cv2.MORPH_RECT, (config['morph']['k_closing'],config['morph']['k_closing']))

mph_flt = None
if config['morph_filter']['enable'] == True:
    mph_flt = filter.areaAspectFilter()
    mph_flt.area_lim = config['morph_filter']['area_lim']
    mph_flt.aspect_lim = config['morph_filter']['aspect_lim']

swt_flt = None
swt_flt = filter.swtFilter(msr.gray_img)

if arg_profile_morph:
    cProfile.run('binaries = mph.morph_operation(binaries, flt=mph_flt, \
                               debug=arg_enable_debug_morph)')
else:
    binaries = mph.morph_operation(binaries, flts=[mph_flt, swt_flt], \
                               debug=arg_enable_debug_morph)


# 创建选区处理实例，并从二值图像中提起候选区域分别保存为图片
ctr = None
if config['contours']['name'] == "car_license":
    ctr = contours.contours_car_license(binaries)
else:
    ctr = contours.tdcontours(binaries)

ctr.t_of_extreme_area_ratio_for_ab = config['contours']['extreme_area_ratio_for_ab']
ctr.t_of_overlap_ratio = config['contours']['overlap_ratio']
ctr.t_of_area_size = config['contours']['area_size']
ctr.t_of_ar_of_direction_type = config['contours']['ar_of_direction_type']
ctr.t_of_distance = config['contours']['distance']
ctr.t_of_merged_aspect_lim = config['contours']['merged_aspect_lim']

if arg_profile_contours:
    cProfile.run('ctr.aggreate_contours(debug=arg_enable_debug_contours, \
                                debug_verbose=arg_enable_debug_contours_verbose)')
else:
    ctr.aggreate_contours(debug=arg_enable_debug_contours, \
                                debug_verbose=arg_enable_debug_contours_verbose)

if config['contours_filter']['enable'] == True:
    ctr_flt = filter.areaAspectFilter()
    ctr_flt.area_lim = config['contours_filter']['area_lim']
    ctr_flt.aspect_lim = config['contours_filter']['aspect_lim']
    ctr.flesh_binaries_using_filtered_boxes(ctr_flt, arg_enable_debug_contours_filter)


# 生成训练数据
if arg_save_region:
    segimgs = ctr.get_detected_segimgs(msr.gray_img)
    # 标记并保存图像
    plt.ion()
    for i,(box,simg) in enumerate(segimgs):
        if arg_save_region==True:
            plt.imshow(simg, "gray")
            plt.pause(0.2)
            judge = input("is text region? : ")
            if judge == 'Y' or judge == 'y':
                cv2.imwrite(arg_save_regions_path+image_name+"-"+str(i)+"-Y.jpg", simg)
            else:
                cv2.imwrite(arg_save_regions_path+image_name+"-"+str(i)+"-N.jpg", simg)
    sys.exit()


# SVM 检测分类
text_regions_binaries = ctr.binaries.copy()
final_result = []
if arg_enable_svm:
    kernel = config['svm']['kernel']
    degree = config['svm']['degree']
    k_c =    config['svm']['k_c']
    gamma =  config['svm']['gamma']

    classification = svm.svc(kernel, gamma, degree, k_c)
    classification.train(arg_training_path)
    segimgs = ctr.get_detected_segimgs(msr.gray_img)
    for si in segimgs:
        ret = classification.predict(si[1])
        if ret =="Y":
            final_result.append(si)
else:
    final_result = ctr.get_detected_segimgs(msr.gray_img)


# 计算 f-measure 评估结果
if arg_enable_eval:
    e = evaluate.evaluate()
    gt_img = cv2.imread(arg_ground_truth_img_path, 0)
    _, gt_img = cv2.threshold(gt_img, 128, 255, cv2.THRESH_BINARY)
    gt_img = cv2.resize(gt_img, (ctr.binaries.shape[1],ctr.binaries.shape[0]))
    precision = e.precision(ctr.boxes, gt_img)
    recall = e.recall(ctr.boxes, gt_img)
    print("\nResult:")
    print("Precision: %.3f\nRecall:%.3f" %(precision, recall))


# 标记最终选区
ret_img = None
if arg_color:
    ret_img = cv2.cvtColor(msr.color_img, cv2.COLOR_RGB2BGR)
elif arg_prep:
    ret_img = cv2.cvtColor(msr.prep_gray_img, cv2.COLOR_GRAY2BGR)
else:
    ret_img = cv2.cvtColor(msr.gray_img, cv2.COLOR_GRAY2BGR)
ret_img = regions.regions.label_image_with_box(ret_img, ctr.get_boxes(), (255,0,0))
for si in final_result:
    ret_img = cv2.drawContours(ret_img, [np.int0(si[0])], 0, (0,255,0), thickness=4)
    
if arg_is_show_result:
    plt.ioff()
    plt.figure(figsize=(10,8))
    plt.imshow(ret_img, "gray")
    plt.show()

if arg_ocolor != "":
    cv2.imwrite(arg_ocolor, cv2.cvtColor(ret_img, cv2.COLOR_BGR2RGB))

if arg_ogray != "":
    cv2.imwrite(arg_ogray, (ret_img))

