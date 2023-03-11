# 参考: https://tora3data.com/prophet/

import numpy as np
import pandas as pd
import datetime
from sklearn import preprocessing
from prophet import Prophet

proph = Prophet()
#proph.add_regressor('高値')
#proph.add_regressor('終値')

kabuka_data = pd.read_csv('./kabuka_6702.csv')
kabuka_data['ds'] = pd.to_datetime(kabuka_data['日付'], format='%Y-%m-%d')
kabuka_data['y'] = kabuka_data['安値']
print(kabuka_data)

proph.fit(kabuka_data[kabuka_data['ds'] < datetime.datetime(2022,1,1,0,0,0,0)])

future = proph.make_future_dataframe(periods=30)

future['高値'] = kabuka_data[:len(future['ds'])]['高値']
future['終値'] = kabuka_data[:len(future['ds'])]['終値']
print(future)

forecast = proph.predict(future)

future['Predict'] = forecast['yhat']
future['安値'] = kabuka_data[:len(future['ds'])]['安値']
print(future)

