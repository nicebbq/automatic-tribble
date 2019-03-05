#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import csv
import os

def strdate_to_intdate(dt):
    date = int(''.join(dt.split('-')))
    return date

def run_file(json_file, csv_file):
    if os.path.exists(csv_file):
        print ("Already exists", csv_file)
        return
    try:
        with open(json_file) as file:
            all = json.load(file)
        
        origin = all["origin"]
        data = all["results"]
        whole = []
        for points in data:
            outList = [origin]
            outList.append(points["destination"])
            outList.append(strdate_to_intdate(points["departure_date"]))
            outList.append(points["price"])
            outList.append(points["airline"])
            whole.append(outList)
        
        with open(csv_file, "w", newline = '') as outFile:
            out = csv.writer(outFile, quoting = csv.QUOTE_ALL)
            for j in whole:
                out.writerow(j)
        print ("Done for ", json_file)
    except:
        print ("No data availabe for ", json_file)
    
base_dir = "/home/fastravel/"    
json_dir = base_dir + "raw_data/flights/"
csv_dir = base_dir + "data/flights/"

if not os.path.exists(csv_dir):
    os.mkdir(csv_dir)
    
for json_file_name in os.listdir(json_dir):
    json_file = json_dir + json_file_name
    csv_file_name = json_file_name.rsplit('.')[0] + '.csv'
    csv_file = csv_dir + csv_file_name
    run_file(json_file, csv_file)
