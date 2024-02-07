from keras.models import Sequential
from keras.layers import LSTM, Dense, TimeDistributed
# from keras.utils import to_categorical
import numpy as np

model = Sequential()

model.add(LSTM(32, return_sequences=True, input_shape=(None, 5)))
model.add(LSTM(8, return_sequences=True))
model.add(TimeDistributed(Dense(2, activation='sigmoid')))

print(model.summary(90))

model.compile(loss='categorical_crossentropy',
              optimizer='adam')

#%%
while True:
    sequence_length = np.random.randint(1,10)
    x_train = np.random.random((10, sequence_length))
    # y_train will depend on past 5 timesteps of x
    y_train = x_train[:, :]
