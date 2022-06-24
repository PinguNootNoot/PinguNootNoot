import numpy as np
import pandas as pd
import random as rd
import glob
from pandas.core.indexes import period
import scipy.io as scyio
import matplotlib.pyplot as plt
import warnings

import cv2
import tensorflow as tf
from tensorflow.keras.applications.resnet import ResNet152
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import backend
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import confusion_matrix
from tensorflow.python.keras.applications.resnet import ResNet152

# GPU Testing
#print(tf.test.is_gpu_available())
#quit()

# Setting up before starting
warnings.filterwarnings('ignore')
onehot = OneHotEncoder()

train_path = './image_set/train_set/'
test_path = './image_set/test_set/'
IMAGE_SIZE = (224,224)

# Preparing Train Dataset
train_img = list()
train_label = list()
val_img = list()
val_label = list()

train_images = sorted(glob.glob(train_path + '*'))
train_images = [x.replace('\\', '/') for x in train_images]

# rd.shuffle(train_images)
# rd.shuffle(val_images)

#for img, i in zip(val_images, brand_df['label']):
#    val_img.append(cv2.resize(cv2.imread(img), IMAGE_SIZE))
#    val_label.append(i)

train_cases = scyio.loadmat('./devkit/cars_train_annos.mat')
for i in range(len(train_images)):
    train_img.append(cv2.resize(cv2.imread(train_path + [item.flat[0] for item in train_cases['annotations'][0][i][5]][0]), IMAGE_SIZE))
    train_label.append([item.flat[0] for item in train_cases['annotations'][0][i][4]][0])

train_img = np.array(train_img)
train_img = train_img / 255

train_label = tf.one_hot(train_label, 196)
train_x = tf.convert_to_tensor(train_img)
train_y = tf.convert_to_tensor(train_label)

#print(train_x)
#print('*-------------------------------------------------------------------------------------*')
#print(train_y)


# Preparing Classifier Model
model = ResNet152(weights='imagenet', input_shape=(224,224,3), include_top=False)
#ModelRes = models.load_model('./ResNet152.h5')

x_top = layers.Flatten()(model.output)
x_top = layers.Dense(1000, activation='relu')(x_top)
prediction = layers.Dense(196, activation='softmax')(x_top)
#model.summary()

ModelRes = Model(inputs=model.input, outputs=prediction)
ModelRes.compile(
    loss='categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)
backend.set_value(ModelRes.optimizer.learning_rate, 0.01)

checkpoint = ModelCheckpoint('./ResNet152.h5', verbose=1, save_weights_only=False, mode='auto', save_freq='epoch', period=10)
result = ModelRes.fit(train_x,
                    train_y,
                    epochs=20,
                    steps_per_epoch=100,
                    validation_steps=10,
                    batch_size=8,
                    validation_split=0.1,
                    callbacks=[checkpoint]
                    )


# Time for Validation
eval_path = './classifier_evaluation/'
CSV_FILENAME = 'group11.csv'

eval_images = sorted(glob.glob(eval_path + '*'))
eval_images = [x.replace('\\', '/') for x in eval_images]
eval_list = list()

image_name = [r.replace('./classifier_evaluation/', '') for r in eval_images]
pred_df = pd.DataFrame(image_name, columns=['filename'])
pred_df['label'] = 0

for img in eval_images:
    eval_list.append(cv2.resize(cv2.imread(img), IMAGE_SIZE))

eval_set = np.array(eval_list) / 255
eval_set = tf.convert_to_tensor(eval_set)

pred_result = model.predict(eval_set)
for i in range(len(pred_result)):
    max = 0
    label = -1
    for j in range(len(pred_result[i])):
        if max < pred_result[i][j]:
            max = pred_result[i][j]
            label = j + 1
    
    pred_df.at[i,'label'] = label

pred_df.to_csv(CSV_FILENAME)
print(pred_df.head())
