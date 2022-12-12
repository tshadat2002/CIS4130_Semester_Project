import numpy as np
import pandas as pd
import boto3

from skimage import color
from skimage.transform import resize
from PIL import Image as im

import os
import io
import joblib
import pickle

from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from yellowbrick.classifier import ROCAUC
from yellowbrick.classifier import ClassificationReport
from yellowbrick.classifier import ClassPredictionError
import matplotlib.pyplot as plt



#connecting to S3 bucket
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('cartoonclassification')

#initializing labels
labels = ['Familyguy',
 'Gumball',
 'Tsubasa',
 'adventure_time',
 'catdog',
 'pokemon',
 'smurfs',
 'southpark',
 'spongebob',
 'tom_and_jerry']

#initializing img size
img_size = 128

def train_data():
    X_train = []
    y_train = []
    for label in labels:
        prefix = os.path.join('cartoon_class/TRAIN', label)
        print(prefix)
        class_num = labels.index(label)
        count = 0
        for obj in my_bucket.objects.filter(Prefix = prefix):
            if count == 3:
                break
            count += 1
            try:
                file_content = obj.get()['Body'].read()
                img = im.open(io.BytesIO(file_content))
                img_arr = np.asarray(img)
                img_arr = color.rgb2gray(img_arr)
                resized_arr = resize(img_arr, (img_size, img_size))
                X_train.append(resized_arr)
                y_train.append(class_num)
            except Exception as e:
                print(e)
    print("LOADED TRAINING DATA")
    X_train = np.asarray(X_train)
    y_train = np.asarray(y_train)
    return X_train, y_train

def test_data():
    X_test = []
    y_test = []
    for label in labels:
        prefix = os.path.join('cartoon_class/TEST', label)
        print(prefix)
        class_num = labels.index(label)
        count = 0
        for obj in my_bucket.objects.filter(Prefix = prefix):
            if count == 3:
                break
            count += 1
            try:
                file_content = obj.get()['Body'].read()
                img = im.open(io.BytesIO(file_content))
                img_arr = np.asarray(img)
                img_arr = color.rgb2gray(img_arr)
                resized_arr = resize(img_arr, (img_size, img_size))
                X_test.append(resized_arr)
                y_test.append(class_num)
            except Exception as e:
                print(e)
    print("LOADED TESTING DATA")
    X_test = np.asarray(X_test)
    y_test = np.asarray(y_test)
    return X_test, y_test

X_train, y_train = train_data()
X_test, y_test = test_data()

X_train = (X_train-np.min(X_train))/(np.max(X_train)-np.min(X_train))
X_test = (X_test-np.min(X_test))/(np.max(X_test)-np.min(X_test))

number_of_train = X_train.shape[0]
number_of_test = X_test.shape[0]

X_train_flatten = X_train.reshape(number_of_train,X_train.shape[1]*X_train.shape[2])
X_test_flatten = X_test.reshape(number_of_test,X_test.shape[1]*X_test.shape[2])

X_train = X_train_flatten.T
X_test = X_test_flatten.T

X_train = X_train.T
X_test = X_test.T

print("Loading in model")
lr = joblib.load('lr.pkl')
y_pred = lr.predict(X_test)
y_test_scores = lr.predict_proba(X_test)

print("Classification Report:")
print(metrics.classification_report(y_test, y_pred))
print("Score:")
print(lr.score(X_test, y_test))

print("")
print("Yellowbrick")
labels = ['Familyguy',
 'Gumball',
 'Tsubasa',
 'adventure_time',
 'catdog',
 'pokemon',
 'smurfs',
 'southpark',
 'spongebob',
 'tom_and_jerry']

model = LogisticRegression(max_iter=3000)
visualizer = ROCAUC(model, classes=labels)

visualizer.fit(X_train, y_train)        # Fit the training data to the visualizer
print("Yellowbrick Score:")
print(visualizer.score(X_test, y_test))        # Evaluate the model on the test data
print("Saving image")
visualizer.show(outpath="ROC.png")                       # Finalize and show the figure and save


visualizer = ClassPredictionError(
    model, classes=labels)
visualizer.fit(X_train, y_train)
print("Yellowbrick Score:")
print(visualizer.score(X_test, y_test))
print("Saving image")
visualizer.show(outpath = "classpredictor.png")

#Class Count Visualization
classes = {'Familyguy': 17504, 'Gumball': 12008, 
             'Tsubasa': 14712, 'adventure_time': 15027, 
             'catdog': 12465, 'pokemon': 14569, 'smurfs': 14906, 
             'southpark': 12196, 'spongebob': 12970, 'tom_and_jerry': 11370}

labels = list(classes.keys())
values = list(classes.values())
fig = plt.figure(figsize = (20, 5))
 
# creating the bar plot
plt.bar(labels, values, color ='maroon',
        width = 0.4, label = values)
 
plt.xlabel("Cartoon")
plt.ylabel("Number of Images")
plt.title("Class Count")

# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center', bbox = dict(facecolor = 'white', alpha =.8))

addlabels(labels, values)

plt.show()

#Training + Testing Data Overview
labels = ["Total", "Training Images", "Test Images"]
values = [137727, 119617, 18110]
fig = plt.figure(figsize = (20, 5))
 
# creating the bar plot
plt.bar(labels, values, color ='blue',
        width = 0.4)
 
plt.xlabel("Data Separation")
plt.ylabel("Number of Images")
plt.title("Overview")

# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center', bbox = dict(facecolor = 'white', alpha =.8))

addlabels(labels, values)

plt.show()











