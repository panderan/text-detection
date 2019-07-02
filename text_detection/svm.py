from text_detection import dlbp
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing
from sklearn.metrics import classification_report

import matplotlib.pyplot as plt
import numpy as np
import cv2

class svc:
    
    def __init__(self,kernel='poly', gamma='scale', degree=19, k_c=1.0):
        self.gamma = gamma
        self.kernel= kernel
        self.degree = degree
        self.k_c = k_c

        self.trained = False
        self.dlbp_ft = None
        self.svc = None

    def train(self, datapath):

        # 构建 DLBP 描述实例
        self.dlbp_ft = dlbp.dlbp_feature()
        k, vtr, labels = self.dlbp_ft.training_k(datapath)
        X_train = np.array(vtr)[:, 0:self.dlbp_ft.k]
        y_train = np.array([i=='Y' and 1 or 0 for i in labels])
        
        # 构建 SVC 分类实例
        self.svc = svm.SVC(kernel=self.kernel, gamma=self.gamma, degree=self.degree, C=self.k_c)
        self.svc.fit(X_train, y_train)

        self.trained = True
    
    def predict(self, gimg):

        vet = self.dlbp_ft.get_dlbp_feature(gimg)
        pre = self.svc.predict(vet.reshape(1,-1))
        return pre[0]==1 and "Y" or "N"
    
    def grid_search(self, train_datapath, tuned_parameters, scores=[None], verbose=False):

        # 构建 DLBP 描述实例
        self.dlbp_ft = dlbp.dlbp_feature()
        k, vtr, labels = self.dlbp_ft.training_k(train_datapath)
        X_train = np.array(vtr)[:, 0:self.dlbp_ft.k]
        y_train = np.array([i=='Y' and 1 or 0 for i in labels])
        skf = StratifiedKFold(n_splits=5)

        best_params = []
        for score in scores:
            print("Tuning hyper-parameters for %s" % score)
            clf = GridSearchCV(svm.SVC(), tuned_parameters, iid=False, cv=skf, scoring=score, n_jobs=-1)
            clf.fit(X_train, y_train)
            best_params.append(clf.best_params_)

            if verbose:
                means = clf.cv_results_['mean_test_score']
                stds = clf.cv_results_['std_test_score']
                for mean, std, params in zip(means, stds, clf.cv_results_['params']):
                    print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
                print()
       
        print("Best parameters:") 
        for scr,bps in zip(scores, best_params):
            print("    %s:\n\t%s"%(scr,bps))
