import joblib
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings('ignore')

# Read list to memory
def read_list(file):
    # for reading also binary mode is important
    with open(file, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list

#loading in training and testing data
X_train, X_test, y_train, y_test = read_list("X_train"), read_list("X_test"), read_list("y_train"), read_list("y_test") 
    
# parameter grid
parameters = {
    'penalty' : ['l1','l2'], 
    'C'       : np.logspace(-3,3,7),
    'solver'  : ['newton-cg', 'lbfgs', 'liblinear'],
}

logreg = LogisticRegression()
clf = GridSearchCV(logreg,                    # model
                   param_grid = parameters,   # hyperparameters
                   scoring='accuracy',        # metric for scoring
                   cv=10)                     # number of folds

clf.fit(X_train,y_train)

print("Tuned Hyperparameters :", clf.best_params_)
print("Accuracy :",clf.best_score_)

# saving new_model
# joblib.dump(clf, 'lr.pkl')