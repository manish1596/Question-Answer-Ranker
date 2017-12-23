from Data_processing import *
import numpy as np
from sklearn import ensemble



def initial_guess(featurevec):
    feat_list=featurevec
    toret=0
    for feat in feat_list:
        toret=toret+feat
    return toret

def function_h(clfvec, featurevec):
    """Thids defines the function 'h'"""
    iters=len(clfvec)+1
    shrinkage=5
    toret=0
    for clf in clfvec:
        toret=toret+clf.predict([featurevec])
    toret=toret*shrinkage
    toret=toret+initial_guess(featurevec)
    toret=toret/iters
    return toret
        

def fragment_S(clfvec, S):
    Splus=[]
    Sminus=[]
    tau=30
    for s in S:
        if function_h(clfvec, s[0].features)>=function_h(clfvec, s[1].features)+tau:
            Splus.append(s)
        else:
            Sminus.append(s)
    return [Splus, Sminus]
    
def train_predictors(clfvec, S):
    Splus,Sminus=fragment_S(clfvec, S)
    tau=30
    X_train=[]
    y_train=[]
    for s in Sminus:
        X_train.append(s[0].features)
        y_train.append(function_h(clfvec, s[1].features)+tau)
        X_train.append(s[1].features)
        y_train.append(function_h(clfvec, s[0].features)-tau)
    params={'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 1, 'learning_rate': 0.05, 'loss': 'ls'}
    clf=ensemble.GradientBoostingRegressor(**params)
    X_train=np.array(X_train)
    y_train=np.array(y_train)
    y_train=y_train.ravel()
    clf.fit(X_train, y_train)
    clfvec.append(clf)
    return clfvec

fea=process_doc("dataTrec99.txt")
print len(fea)
segf=segregate_features(fea)
S=create_S(segf)
clfvec=[]

Splus,Sminus=fragment_S(clfvec,S)
print "previous count=",len(Splus)

max_rec_Splus=0
for i in range(5):
    clfvec=train_predictors(clfvec, S)
    Splus,Sminus=fragment_S(clfvec,S)
    if len(Splus)>max_rec_Splus:
        max_rec_Splus=len(Splus)
    print "Iteration "+str(i+1)+" has been completed"+ "Value of len(Splus)="+str(len(Splus))  

print "Length of the clfvec vector so found is =", len(clfvec)



Splus,Sminus=fragment_S(clfvec,S)
print "max rec count=", max_rec_Splus
print "total=",len(S)

