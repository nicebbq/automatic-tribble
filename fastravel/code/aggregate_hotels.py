#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 17:44:01 2018

@author: olya
"""

import pandas as pd
import os

base_dir = '/home/fastravel/'
data_dir = base_dir + 'data/hotels/'
out_name = 'hotels'

files = [filee for filee in os.listdir(data_dir) if filee.rsplit('.',1)[1]=='csv']
cities = sorted(set([file.split('_')[0] for file in files]))
for city in cities:
    if len(city)>3:
        continue
    print (city)
    out_file = data_dir + out_name + '_' + city + '.csv'
    df = pd.DataFrame()
    for file in files:
        if not '--' in file:
            continue
        #print (file)
        city_code = file.split('.')[0].split('--')[0].rsplit('_',1)[0]
        date_str = file.split('--')[0].split('_')[1]
        date = int(''.join(date_str.split('-')))
        if not city in file:
            continue
        try:
            dfi = pd.read_csv(data_dir + file, header=None)
            dfi['c_code'] = city_code
            df = pd.concat([df, dfi], axis=0)
        except:
            continue
    df.columns = ['h_code', 'h_name', 'street', 'city', 'state', 'zip', 'price', \
                  'rate', 'room_code', 'roh', 'room_type', 'bed_type', 'n_beds', 'date', 'c_code']
    df = df[['c_code', 'date', 'h_code', 'h_name', 'street', 'city', 'state', 'zip', 'price', \
                  'rate', 'room_code', 'roh', 'room_type', 'bed_type', 'n_beds']]
    df = df.sort_values(by=['c_code', 'h_code' ,'date'], axis=0)
    df.to_csv(out_file, index=False)
    print ("Done for ", city, len(df))
