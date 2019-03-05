#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 17:44:01 2018

@author: olya
"""

import pandas as pd
import os

def get_dates(files):
    dates = list()
    for file in files:
        date = file.split('.')[0].split('_')[-1]
        if check_date(date):
            dates.append(date)
    return sorted(set(dates))

def check_date(s):
    try:
        d = int(''.join(s.split('-')))
        if d > 20170000 and d < 20200000:
            return True
        return False
    except:
        return False

base_dir = '/home/fastravel/'
data_dir = base_dir + 'data/weather/'
out_name = 'weather_pred'
mode = 'all_dates'    # to aggregate all dates
mode = 'last_date'      # to aggregate the last date

files = os.listdir(data_dir)
dates = get_dates(files)
if mode=='last_date':
    dates = [dates[-1]]
df0 = pd.read_csv(data_dir + files[0])
cols = ['code']
cols.extend(list(df0.columns))
cols.append('pred_date')
for date in dates:
    out_file = data_dir + out_name + '_' + date + '.csv'
    df = pd.DataFrame()
    for file in files:
        city_code = file.split('_')[0]
        if not date in file:
            continue
        dfi = pd.read_csv(data_dir + file)
        dfi['pred_date'] = int(''.join(date.split('-')))
        dfi['code'] = city_code
        df = pd.concat([df, dfi], axis=0)
        df['datetime'] = df['date'] * 1000000 + df['time']
    df = df.sort_values(by=['code','datetime'], axis=0)
    df = df[cols]
    df.to_csv(out_file, index=False)
    print ("Done for ", date)
