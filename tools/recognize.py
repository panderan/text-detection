from text_detection import dlbp
from sklearn import svm
import numpy as np
import cv2

filenames = open("filenames.txt", 'r')
files = filenames.readlines()
files = map(lambda x:x[0:-1], files)
maskfilenames = open("maskFilenames.txt", 'r')
masks = maskfilenames.readlines()
masks = map(lambda x:x[0:-1], masks)

ddd = dlbp.dlbp_feature() 
k,vtr,labels = ddd.training_k("IDCards/Rear/Training")
training_data = np.array(vtr)[:,0:ddd.k]
clf = svm.SVC(gamma='scale', kernel='poly')
clf.fit(training_data, labels)

for f,fm in list(zip(files,masks)):
    gimg = cv2.imread(f,0)
    gimg_msk = cv2.imread(fm,0)
    vet = ddd.get_dlbp_feature(gimg, gimg_msk)
    pre = clf.predict(np.array(vet).reshape(1,-1))
    print(f+" : "+str(pre[0]))
