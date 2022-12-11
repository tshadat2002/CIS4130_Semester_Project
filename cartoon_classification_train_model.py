import joblib
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

# Read list to memory
def read_list(file):
    # for reading also binary mode is important
    with open(file, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list

print("Reading in data")
X_train, X_test, y_train, y_test = read_list("X_train"), read_list("X_test"), read_list("y_train"), read_list("y_test") 
    
#training model with default parameters
lr = LogisticRegression(max_iter = 1500)
lr.fit(X_train, y_train)

#saving model
joblib.dump(lr, 'lr.pkl')


#evaluating model
y_pred = lr.predict(X_test)
print(lr.score(X_test, y_test))
print(metrics.classification_report(y_test, y_pred))