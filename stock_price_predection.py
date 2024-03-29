# -*- coding: utf-8 -*-
"""stock price predection.ipynb

## **Importing Libraries**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""## **Loading Our Dataset**"""

from google.colab import files

dataset = files.upload()

df = pd.read_csv('TSLA.csv')

"""## **Feature Extraction**

The number of the trading days and the columns:
"""

df.shape

df = df['Open'].values
df = df.reshape(-1, 1)

"""After extracting one column:

"""

df.shape

dataset_train = np.array(df[:int(df.shape[0]*0.8)])
dataset_test = np.array(df[int(df.shape[0]*0.8):])
print(dataset_train.shape)
print(dataset_test.shape)

"""Importing our model:"""

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout

"""Scaling data:"""

scaler = MinMaxScaler(feature_range=(0,1))
dataset_train = scaler.fit_transform(dataset_train)
dataset_train[:5]

dataset_test = scaler.transform(dataset_test)
dataset_test[:5]

def create_dataset(df):
    x = []
    y = []
    for i in range(50, df.shape[0]):
        x.append(df[i-50:i, 0])
        y.append(df[i, 0])
    x = np.array(x)
    y = np.array(y)
    return x,y

"""Creating training and testing datasets:"""

x_train, y_train = create_dataset(dataset_train)
x_test, y_test = create_dataset(dataset_test)

"""Creating our LSTM model:"""

model = Sequential()
model.add(LSTM(units=96, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=96))
model.add(Dropout(0.2))
model.add(Dense(units=1))

"""Reshape features for the LSTM layer:"""

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

model.compile(loss='mean_squared_error', optimizer='adam')

"""Start the training:"""

model.fit(x_train, y_train, epochs=50, batch_size=32)
model.save('stock_prediction.h5')

model = load_model('stock_prediction.h5')

"""## **Results visualization**"""

predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)
y_test_scaled = scaler.inverse_transform(y_test.reshape(-1, 1))

fig, ax = plt.subplots(figsize=(16,8))
ax.set_facecolor('#000041')
ax.plot(y_test_scaled, color='red', label='Original price')
plt.plot(predictions, color='cyan', label='Predicted price')
plt.legend()
