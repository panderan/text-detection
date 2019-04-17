from text_detection import mser, filter, morph, contours
import matplotlib.pyplot as plt
import cv2
import sys

IMAGE_PATH = sys.argv[1]
msr = mser.mser_cls(IMAGE_PATH)
flt = filter.mser_filter400k(msr.gray_img)
rect, binaries = msr.extraction_with_labels(flt = flt)
#rect, binaries, colorized, msers, bboxes = msr.extraction_with_labels_verbose(flt = flt)
#binaries = morph.morph.opening(binaries)
kl = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
binaries = cv2.dilate(binaries, kl)
binaries = morph.morph.closeing(binaries)

ctr = contours.tdcontours(binaries)
#ctr.get_contours_verbose()
ctr.save_each_contours(msr.gray_img)


#plt.imshow(binaries)
#plt.show()
