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
        try:
            date = file.split('.')[0].split('--')[0].rsplit('_',1)[1]
            dates.append(date)
        except:
            pass
    return sorted(set(dates))

base_dir = '/home/fastravel/'
data_dir = base_dir + 'data/flights/'
out_name = 'flights'
mode = 'all_dates'    # to aggregate all dates
#mode = 'last_date'      # to aggregate the last date

files = [filee for filee in os.listdir(data_dir) if filee.rsplit('.',1)[1]=='csv']
dates = get_dates(files)
if mode=='last_date':
    dates = [dates[-1]]
for date in dates:
    out_file = data_dir + out_name + '_' + date + '.csv'
    df = pd.DataFrame()
    for file in files:
        cities_codes = file.split('.')[0].split('--')[0].rsplit('_',1)[0]
        if not date+'--' in file:
            continue
        dfi = pd.read_csv(data_dir + file, header=None)
        df = pd.concat([df, dfi], axis=0)
    df.columns = ['origin', 'destin', 'date', 'price', 'airline']
    df = df.sort_values(by=['origin','destin','date'], axis=0)
    df.to_csv(out_file, index=False)
    print ("Done for ", date, len(df))
