#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import numpy as np
import pandas as pd

def int_to_date(i):
    day = int (i % 100)
    year = int(i / 10000)
    month = int ((i % 10000) / 100)
    return dt.date(year, month, day)

def date_to_int(d):
    return d.year * 10000 + d.month * 100 + d.day

def num_to_main(x):
    if x == 0:
        return 'Clear'
    if x == 1:
        return 'Clouds'
    if x == 2:
        return 'Rain'

pred_path = '../data/weather/weather_predict1.npy'
cities_path = '../data/weather/cities_list.txt'
last_data = '../data/weather/weather_pred_2018-07-30.csv'
output_path = '../data/weather/weather_aggregate_pred.csv'

pred_attrs = ['temp', 'pressure', 'humidity', 'main', 'rain_3h']
all_attrs = ['code', 'date', 'time', 'temp', 'temp_min', 'temp_max', 'pressure', \
             'humidity', 'temp_kf', 'main', 'description', 'clouds', 'wind_speed', 'rain_3h', 'pred_date']
n_points_per_day = 8
#n_original_days = 5
n_original_points = 40  # 5 days every 3 hours

#df = pd.read_csv(last_pred)
#df = df.drop_duplicates(subset=['code'], keep='last')
#print (df.iloc[:,:5])

last_pred_date = 20180801
last_pred_time = 210000
n_1st_day_skipped_points = int (last_pred_time / 30000 + 1)

start_date = int_to_date(last_pred_date)

pred = np.load(pred_path)
n_periods = pred.shape[1]
n_pred_periods = n_periods - n_original_points
n_pred_dates = int(n_pred_periods / 8) + 1
pred_times = list(range(0, 220000, 30000)) * n_pred_dates
pred_times = pred_times[n_1st_day_skipped_points:]
pred_times = pred_times[:n_pred_periods]
pred_dates = [date for d in range(n_pred_dates) for date in ([date_to_int(start_date + dt.timedelta(days=d))] * n_points_per_day)]
pred_dates = pred_dates[n_1st_day_skipped_points:]
pred_dates = pred_dates[:n_pred_periods]
n_cities = pred.shape[0]

cities = list(pd.read_csv(cities_path, header=None).iloc[:,0])
df_res = pd.DataFrame(columns = all_attrs)
for i in range(n_cities):
    city = cities[i]
    print (i, cities[i])
    city_data = pred[i,:,:]
    df = pd.DataFrame(city_data)
    df.columns = pred_attrs
    df = df[n_original_points:]
    df['date'] = pred_dates
    df['time'] = pred_times
    df['code'] = city
    df_res = pd.concat([df_res, df], axis=0)
df_res = df_res[all_attrs]
df_res = df_res.set_index('code')
df_res['rain_3h'][df_res['main']<2] = 0.
df_res['main'] = df_res['main'].map(lambda x: num_to_main(x))
df_res.to_csv(output_path)
#print (df_res.head(), '\n', df_res.tail(), len(df_res))
#print (set(df_res['main']))
