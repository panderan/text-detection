from text_detection import lbp
from sklearn import svm
import numpy as np
import cv2

filenames = open("filenames.txt", 'r')
files = filenames.readlines()
files = map(lambda x:x[0:-1], files)
maskfilenames = open("maskFilenames.txt", 'r')
masks = maskfilenames.readlines()
masks = map(lambda x:x[0:-1], masks)

lbp_intance = lbp.lbp()
trainingdata, label = lbp_intance.get_training_data("IDCards/Rear/Training")

clf = svm.SVC(gamma='scale', kernel='poly')
clf.fit(trainingdata, label)

for f,fm in list(zip(files,masks)):
    gimg = cv2.imread(f,0)
    gimg_msk = cv2.imread(fm,0)
    vet = lbp_intance.get_lbp_feature(gimg, gimg_msk)
    pre = clf.predict(np.array(vet).reshape(1,-1))
    print(f+" : "+str(pre[0]))
