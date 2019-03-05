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
#def strdate_to_intdate(dt):
    #date = int(''.join(dt.split('-')))
    #return date

#def run_file(json_file, csv_file):
    #try:
with open("testMulti.json") as file:		##change this
	all = json.load(file)
	#all = json.load("testHotels.json")
        
        #origin = all["origin"]
data = all["results"]
whole = []
for points in data:
    outList = []
    outList.append(points["property_name"])
    addr = points["address"]
    #outList.append(strdate_to_intdate(points["departure_date"]))
    outList.append(addr["line1"])
    outList.append(addr["city"])
    outList.append(addr["region"])
    outList.append(addr["postal_code"])
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
		#try:
		#	theRoom.append(rooms["room_type_info"]["room_type"])
		#except:
		theRoom.append(roomParse(roomCode[0]))
		try:
			theRoom.append(rooms["room_type_info"]["bed_type"])
		except:
			theRoom.append(bedParse(roomCode[2]))
		try:
			theRoom.append(rooms["room_type_info"]["number_of_beds"])
		except:
			theRoom.append(numParse(roomCode[1]))
	whole.append(outList + theRoom)
			
    #outList.append(points["airline"])
    #whole.append(outList)

with open("HotelsMulti.csv", "w") as outFile:	##change this
    out = csv.writer(outFile, quoting = csv.QUOTE_ALL)
    for j in whole:
	out.writerow(j)
print ("Done for ", json_file)
    #except:
        #print ("No data availabe for ", json_file)
    
    
#json_dir = "../raw_data/hotels/"
#csv_dir = "../data/hotels/"

#if not os.path.exists(csv_dir):
    #os.mkdir(csv_dir)
    
#for json_file_name in os.listdir(json_dir):
    #json_file = json_dir + json_file_name
    #csv_file_name = json_file_name.rsplit('.')[0] + '.csv'
    #csv_file = csv_dir + csv_file_name
    #run_file(json_file, csv_file)
