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
            if count == 10:
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
            if count == 10:
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

# write list to binary file
def write_list(a_list, file_name):
    # store list in binary file so 'wb' mode
    with open(file_name, 'wb') as fp:
        pickle.dump(a_list, fp)
        print('Done writing list into a binary file')

write_list(X_train, "X_train")     
write_list(X_test, "X_test")        
write_list(y_train, "y_train")        
write_list(y_test, "y_test")        

        
    











