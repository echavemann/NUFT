import math
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Dense
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from sklearn.preprocessing import MinMaxScaler 

class BaseModel:

	def __init__(self):
		self.data = []
		self.data_copy = []
		self.train = []
		self.test = []
		self.features = []
		self.filtered_data = []
		self.data_pred = []
		self.pred = ''
		self.feature_scaler = None
		self.pred_scaler = None
		self.normalized_data = None
		self.normalized_pred = None
		self.model = None
		self.x_test =[]
		self.y_test =[]
		self.x_train =[]
		self.y_train = []

	def load_dataframe(self,df,Features=['High', 'Low', 'Open', 'Close', 'Volume'],sort_by='Date',pred='Close'):
	# this function loads dataframe into 
		self.data = df 
		self.data_copy = self.data.copy()
		self.features = Features
		self.pred = pred
		print('Visualizing DataFrame...')
		self.visualize_data()
		print('Cleaning Data...')
		self.clean_data(features=Features,by=sort_by)
		print('Normalizing Data...')
		self.normalize_data()
		self.train, self.test = self.split_train_test(frac=0.8)

	def clean_data(self,features,by='Date'):
	# this function removes the unwanted columns in the dataframe after sorting by date
		train_df = pd.sort_values(by=[by]).copy()
		date_index = train_df.index
		train_df = train_df.reset_index(drop=True).copy()
		data = pd.DataFrame(train_df)
	# set the class's filtered data to the data with specified features
		self.filtered_data = data[features]
	# add a prediction column
		self.data_pred = self.filtered_data.copy()
		self.data_pred['Prediction'] = self.data_pred[self.pred]


	def visualize_data(self):
		list_length = self.data.shape[1] # number of features in dataframe
		ncols = 2
		nrows = int(round(list_length / ncols, 0))
		fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, figsize=(10, 7))
		for i in range(0, list_length):
			ax = plt.subplot(nrows,ncols,i+1) # create a set of plots
			sns.lineplot(data = self.data)
			ax.set_title(self.data.columns[i]) # give titles to graphs
			ax.xaxis.set_major_locator(mdates.AutoDateLocator()) # label x axis of graphs
		plt.show()



	def normalize_data(self):
	# helper function that uses min-max scaler for normalizing the data
	# this step is necessary for a better performance
		nrows = self.data_filtered.shape[0]
		np_data_unscaled = np.array(self.data_filtered)
		np_data = np.reshape(np_data_unscaled, (nrows, -1))
		self.feature_scaler = MinMaxScaler()
		self.normalized_data = self.feature_scaler.fit_transform(np_data_unscaled)
		self.pred_scaler = MinMaxScaler()
		pred = pd.DataFrame(self.filtered_data['Close'])
		self.normalized_pred = self.pred_scaler.fit_transform(pred)

	def plot_pred(self, ):
		# predict with the model we trained
		y_pred_scaled = self.model.predict(self.x_test)
		# transform prediction back to the original scale
		y_pred = self.pred_scaler.inverse_transform(y_pred_scaled)
		# transform y_test back to the original scale
		y_test_unscaled = self.pred_scaler.inverse_transform(y_pred.reshape(-1, 1))

		plt.plot(y_pred)
		plt.plot(y_test_unscaled)
		plt.title('Performance of model')
		plt.grid()
		plt.legend(['Predicted','Actual Value'])

	def partition_dataset(self, sequence_length, data, index_close):
		x, y = [], []
		data_len = self.data_copy.shape[0]
		for i in range(sequence_length, data_len):
			x.append(self.data_copy[i-sequence_length:i,:]) #contains sequence_length values 0-sequence_length * columsn
			y.append(self.data_copy[i, index_close]) #contains the prediction values for validation,  for single-step prediction
	    # Convert the x and y to numpy arrays
		x = np.array(x)
		y = np.array(y)
		return x, y

	def train_test_split(self,frac=0.8,sequence_length=50):
		index_close = self.data_copy.columns.get_loc(self.pred)
		train_data_len = math.ceil(self.normalized_data.shape[0] * frac)
		train_data = self.normalized_data[0:train_data_len, :]
		test_data = self.normalized_data[train_data_len - sequence_length:, :]
		self.x_train, self.y_train = self.partition_dataset(sequence_length,train_data,index_close)
		self.x_test, self.y_test = self.partition_dataset(sequence_length,test_data,index_close)

	def initialize_model(self):
		self.model = Sequential()

	def naive_model(self):
		# very naive model
		self.model.add(LSTM(units=50, return_sequences=True, input_shape=(self.x_train.shape[1], self.x_train.shape[2]))) 
		self.model.add(LSTM(units=50, return_sequences=True))
		self.model.add(LSTM(units=50, return_sequences=False))
		self.model.add(Dense(5))
		self.model.add(Dense(1))
		# Compile the model
		self.model.compile(optimizer='adam', loss='mse')
		history = self.model.fit(self.x_train, self.y_train, 
                    batch_size=32, 
                    epochs=50,
                    validation_data=(self.x_test, self.y_test)
                   )

