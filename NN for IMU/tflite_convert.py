# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 11:06:01 2023

@author: Administrator
"""

import tensorflow as tf
import os
os.chdir(r'F:\py_code\Py3\NN for IMU')
# Convert the model

model = tf.keras.models.load_model("LSTM1.keras")

# converter = tf.lite.TFLiteConverter.from_saved_model('LSTM1') # path to the SavedModel directory

converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open('model.tflite', 'wb') as f:
  f.write(tflite_model)