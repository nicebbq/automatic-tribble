#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import csv
import os

def roomParse(code):
	if(code == "I" or code == "J" or code ==  "K"):
		return "No"
	elif(code == "C"):
		return "Varies"
	else:
		return "Yes"

def bedParse(code):
	if(code == "S"):
		return "Single"
	if(code == "T"):
		return "Twin"
	if(code == "D"):
		return "Double"
	if(code == "Q"):
		return "Queen"
	if(code == "K"):
		return "King"
	if(code == "C"):
		return "Varies"
	return "Other"

def numParse(code):
	if(code == "C"):
		return "Varies"
	try: 
		float(code)
		return code
	except:
		return "Unknown"
    
def getDate(json_file):
    date = json_file.split('.')[0].split('--')[0].rsplit('_',1)[1]
    date = int(''.join(date.split('-')))
    return date
    
def run_file(json_file, csv_file):
    #print (json_file, '\t', csv_file)
    with open(json_file) as file:
        all = json.load(file)
        
    date = getDate(json_file)
    
    try:    
        data = all["results"]
    except:
        print ("No data available in ", json_file)
        return
    whole = []
    for points in data:
        outList = []
        outList.append(points["property_code"])
        outList.append(points["property_name"])
        addr = points["address"]
        outList.append(addr["line1"])
        outList.append(addr["city"])
        outList.append(addr["region"])
        try:
            outList.append(addr["postal_code"])
        except:
            outList.append("")
        roomData = points["rooms"]
        for rooms in roomData:
            theRoom = []
            theRoom.append(rooms["rates"][0]["price"])
            theRoom.append(rooms["rate_plan_code"])
            roomCode = rooms["room_type_code"]
            theRoom.append(roomCode)
            if(roomCode == "ROH"):
                theRoom.append("Yes")
                theRoom.append("Varies")
                theRoom.append("Varies")
                theRoom.append("Varies")
            else:
                theRoom.append("No")
                try:
                    theRoom.append(rooms["room_type_info"]["room_type"])
                except:
                    theRoom.append("unknown")
#                theRoom.append(roomParse(roomCode[0]))
                try:
                    theRoom.append(rooms["room_type_info"]["bed_type"])
                except:
                    theRoom.append(bedParse(roomCode[2]))
                try:
                    theRoom.append(rooms["room_type_info"]["number_of_beds"])
                except:
                    theRoom.append(numParse(roomCode[1]))
            theRoom.append(date)
        whole.append(outList + theRoom)
			
    with open(csv_file, "w") as outFile:
        out = csv.writer(outFile, quoting = csv.QUOTE_ALL)
        for j in whole:
            out.writerow(j)
    print ("Done for ", json_file)
    #except:
        #print ("No data availabe for ", json_file)
    
base_dir = "/home/fastravel/"
json_dir = base_dir + "/raw_data/hotels/"
csv_dir = base_dir + "/data/hotels/"

if not os.path.exists(csv_dir):
    os.mkdir(csv_dir)
    
for json_file_name in os.listdir(json_dir):
    json_file = json_dir + json_file_name
    csv_file_name = json_file_name.rsplit('.')[0] + '.csv'
    csv_file = csv_dir + csv_file_name
    run_file(json_file, csv_file)
