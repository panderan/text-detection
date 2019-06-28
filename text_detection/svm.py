from text_detection import dlbp
from sklearn import svm
import matplotlib.pyplot as plt
import numpy as np
import cv2

class svc:
    
    def __init__(self, gamma='scale', kernel='poly', degree=10):
        self.gamma = gamma
        self.kernel= kernel
        self.degree = degree
        self.trained = False
        self.dlbp_ft = None
        self.svc = None

    def train(self, datapath):

        # 构建 DLBP 描述实例
        self.dlbp_ft = dlbp.dlbp_feature()
        k, vtr, labels = self.dlbp_ft.training_k(datapath)
        training_data = np.array(vtr)[:, 0:self.dlbp_ft.k]
        
        # 构建 SVC 分类实例
        self.svc = svm.SVC( gamma=self.gamma, \
                            kernel=self.kernel,\
                            degree=self.degree)
        self.svc.fit(training_data, labels)

        self.trained = True
    
    def predict(self, gimg):

        vet = self.dlbp_ft.get_dlbp_feature(gimg)
        pre = self.svc.predict(np.array(vet).reshape(1,-1))
        return pre[0]

