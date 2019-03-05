#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import csv
import os

def dt_to_datetime(dt):
    datetime = dt.split(' ')
    date = int(''.join(datetime[0].split('-')))
    time = int(''.join(datetime[1].split(':')))
    return date, time

def run_file(json_file, csv_file):
    print ("Running for   ", json_file)
    with open(json_file) as file:
        all = json.load(file)
    
    data = all["list"]
    whole = []
    main_factors = ["temp", "temp_min", "temp_max", "pressure", "humidity", "temp_kf"]
    weather_factors = ["main", "description"]
    factors = ['date', 'time']
    factors.extend(main_factors)
    factors.extend(weather_factors)
    factors.extend(['clouds','wind_speed', 'rain_3h'])
    whole.append(factors)
    for points in data:
        outList = []
        date, time = dt_to_datetime(points["dt_txt"])
        outList.extend([date, time])
        for factor in main_factors:
            outList.append(points["main"][factor])
        for factor in weather_factors:
            outList.append(points["weather"][0][factor])
        outList.append(points["clouds"]["all"])
        outList.append(points["wind"]["speed"])
        try:
            outList.append(points["rain"]["3h"])
        except:
            outList.append(0)
        whole.append(outList)
    #print(whole)
    
    #with open(csv_file, "w", newline = '') as outFile:
    with open(csv_file, "w") as outFile:
        out = csv.writer(outFile, quoting = csv.QUOTE_ALL)
        for j in whole:
            out.writerow(j)
    #print ("Done for ", json_file)
    
    
json_dir = "/home/fastravel/raw_data/weather/"
csv_dir = "/home/fastravel/data/weather/"

if not os.path.exists(csv_dir):
    os.mkdir(csv_dir)
    
for json_file_name in os.listdir(json_dir):
    json_file = json_dir + json_file_name
    csv_file_name = json_file_name.rsplit('.')[0] + '.csv'
    csv_file = csv_dir + csv_file_name
    run_file(json_file, csv_file)
