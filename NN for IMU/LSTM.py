# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 12:25:29 2023

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# Importing the libraries
# from sklearn.preprocessing import MinMaxScaler


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional, Masking
from tensorflow.keras.optimizers import SGD
from tensorflow.random import set_seed

set_seed(455)

import numpy as np
import tensorflow as tf

import numpy as np
import random
import matplotlib.pyplot as plt
import os
np.random.seed(455)

#%% load and format the data
import scipy.io as sio

path = r"E:\Python code\Py3\NN for IMU"       
os.chdir(path)
sigma = sio.loadmat("sigma.mat")
sigmaX = sigma["sigmaX"]
sigmaT = sigma["sigmaT"]

training_dim = np.array([1,2,3,4,6])-1

path = r"E:\Python code\Py3\NN for IMU\data_set\Inputs"
os.chdir(path)
features = {"1":[], "2":[], "3":[], "4":[], "5":[]}

L_max = 325
sample_length = []
sample_num = 0
input_sets = -10*np.ones((89, L_max, 5))

for file in os.listdir(): 
    # Check whether file is in text format or not 
    if file.endswith(".mat"):
        data_i = sio.loadmat(file)["inputs"][training_dim,:]/sigmaX
        sample_length.append(data_i.shape[1])
        # All data sets are padded to the max length
        for dim in range(len(training_dim)):
            # features[str(dim+1)].append(data[training_dim.item(dim),:])
            input_sets[sample_num,:data_i.shape[1], dim] = data_i[dim,:]
        sample_num += 1

#%%    
path = r"E:\Python code\Py3\NN for IMU\data_set\Targets"
os.chdir(path)
target_sets = -10*np.ones((89, L_max, 1))
i = 0
for file in os.listdir(): 
    if file.endswith(".mat"): 
        data = sio.loadmat(file)["targets"]/sigmaT
        L_k = data.shape[1]
        target_sets[i,:L_k, 0] = data
        i += 1

#%%
 # split data into training and test groups      
  
# N = len(target_sets)
# train_ratio = 0.75
# sample_index = np.array([i for i in range(N)])
# random.shuffle(sample_index)
# N_train = round(train_ratio*N)
# train_inputs = input_sets[sample_index[:N_train], :, :]
# train_targets = target_sets[sample_index[:N_train]]
# test_inputs = input_sets[sample_index[N_train:], :, :]
# test_targets = target_sets[sample_index[N_train:]]

train_idx = np.concatenate((np.arange(40), np.arange(50,80)), axis=0)
test_idx = np.concatenate((np.arange(40,50), np.arange(80,89)), axis=0)
train_inputs = input_sets[train_idx, :, :]
train_targets = target_sets[train_idx]
test_inputs = input_sets[test_idx, :, :]
test_targets = target_sets[test_idx]

#%%  LSTM
model = Sequential()
# model.add(tf.keras.Input(shape=(16,)))
# model.add(LSTM(50, input_shape=(None, len(training_dim))))
model.add(Masking(mask_value= -10))
# model.add(LSTM(50, return_sequences=True, input_shape=(None, len(training_dim))))
model.add(GRU(50, return_sequences=True, input_shape=(None, len(training_dim))))
model.add(Dense(40, activation='tanh'))
model.add(Dropout(0.6))
model.add(Dense(1))

model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['mse'])
                    # mean_squared_error
model.fit(train_inputs, train_targets, batch_size= 1, epochs= 50)
# model.fit(input_list, target_list, batch_size= 1, epochs= 1)
# model.fit_generator(MyBatchGenerator(X, y, batch_size=1), epochs=2)

#%% load trained NN
# model = tf.keras.models.load_model("LSTM1.keras")

#%% output of entire sequence
# test_pred = model.predict_on_batch(test_inputs)

# one time step
test_pred = model.predict(test_inputs[1,0:10,:].reshape(1,-1,5))

#%% plot
data_input = test_targets[0,:,0]
x = np.arange(data_input.shape[0])
plt.plot(x, data_input)
plt.show()            

#%%
from sklearn.metrics import mean_squared_error
rmse = []
for _ in range(test_pred.shape[0]):
    data_plot = test_pred[_,:,0]
    target = test_targets[_,:,0]  
    try:
        end_ind = np.where(target == -10)[0][0]
    except:
        end_ind = 325
        
    rmse.append(mean_squared_error(target[:end_ind], data_plot[:end_ind], squared=True) )
    
    x = np.arange(data_plot[:end_ind].shape[0])
    plt.plot(x, data_plot[:end_ind] , label = 'prediction')
    
    data_ref = test_targets[_,:end_ind]
    plt.plot(x, data_ref, label = 'ref')
    plt.legend()
    plt.show()

#%%
os.chdir(r"E:\Python code\Py3\NN for IMU")
model.save('GRU1.keras')

#%%
filename = input('enter the file name: ')       
file = open(filename + '_rmse.txt', 'w')
np.savetxt(file, np.array(rmse))
file.close()

#%%  tensorflow lite
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]
# converter._experimental_lower_tensor_list_ops = False

# tflite_model = converter.convert()

# # Save the model.
# with open('model.tflite', 'wb') as f:
#   f.write(tflite_model)
