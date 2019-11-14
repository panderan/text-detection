#!/usr/bin/env python

import cv2
import gui.text_detection.morph_ops as mo
import matplotlib.pyplot as plt

image = cv2.imread("/root/extract.png", cv2.IMREAD_GRAYSCALE)

morhper = mo.TdMorphOperator()
ret = morhper.morph_operation(image)
print(ret)
