import boto3
from PIL import Image as im
import numpy as np
import io
s3 = boto3.resource('s3')
objects = list(s3.Bucket('cartoonclassification').objects.all())
objects.remove(s3.ObjectSummary(bucket_name='cartoonclassification', key='test.zip'))
test_images = 0
train_images = 0

for x in objects:
    if "TEST" in x.key[14:21]:
        test_images += 1
    elif "TRAIN" in x.key[14:21]:
        train_images += 1

classes = {}
for x in objects:
    clas = x.key.split('/')[2]
    if clas not in classes:
        classes[clas] = 1
    else:
        classes[clas] += 1

avg_width = 0
max_width = -float('inf')
min_width = float('inf')
avg_height = 0
max_height = -float('inf')
min_height = float('inf')
seen = []

for obj in objects:
     clas = obj.key.split('/')[2]
     if clas not in seen:
        file_content = obj.get()['Body'].read()
        img = im.open(io.BytesIO(file_content))
        img_arr = np.asarray(img)


        width, height = img_arr.shape[:2]
        max_width = max(width, max_width)
        min_width = min(width, min_width)
        avg_width += width
        max_height = max(height, max_height)
        min_height = min(height, min_height)
        avg_height += height
        seen.append(clas)

avg_height //= len(classes)
avg_width //= len(classes)

print(f"""Total Number of Images: {len(objects)}

Total Number of Images Used for Training: {train_images}

Total Number of Images Used for Testing: {test_images}

Total Number of Classes: {len(classes)}

Total Number of Images Per Class: 
{classes}

Maximum Height of Images: {max_height}

Maximum Width of Images: {max_width}

Minumum Height of Images: {min_height}

Minimum Width of Images: {min_width}

Average Height of Images: {avg_height}

Average Width of Images: {avg_width}""")
