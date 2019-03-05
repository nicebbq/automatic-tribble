import pymysql
import mysql.connector as mariadb
import string
import random
import numpy as np
from passlib.hash import sha256_crypt as sha


def myGenerator(numtoGen):
	cnct = mariadb.connect(user = 'root', password = '', database = 'fastravel')
	cur = cnct.cursor()
	getCities = "SELECT code from Cities"
	cur.execute(getCities,)
	cities = cur.fetchall()
	#print(cities)
	#print(cities[0][0])
	mu = 150
	sigma = 100
	budgets = np.round(np.random.normal(mu, sigma, numtoGen), decimals = 0)
	#print(budgets)
	
	for i in range(numtoGen):
		length = random.randint(6,25)
		#print (length)
		email = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in xrange(length))
		email = email + "@fakefake.com"
		#print("email: "+ email)
		password = "onions"
		cnct = mariadb.connect(user = 'root', password = '', database = 'fastravel')
		cur = cnct.cursor()
		namecheck = "SELECT Login.email FROM Login WHERE Login.email = %s"
		cur.execute(namecheck, (email,))
		names = cur.fetchall()
		if(names == []):
			add = "INSERT INTO Login VALUES (%s, %s)"
			cur.execute(add, (email, sha.encrypt(password)))
			cnct.commit()
			cur.close()
			cnct.close()
		else:
			cur.close()
			cnct.close()
			continue
		city = str(random.choice(cities)[0])
		date = "2018"+str(random.randint(8,12)).zfill(2) + str(random.randint(1,25)).zfill(2)
		date2 = int(date) + random.randint(1,5)#"2018"+str(random.randint(8,12)).zfill(2) + str(random.randint(1,30)).zfill(2)
		startDate = date
		endDate = date2
		swapChance = random.randint(1,100)
		if swapChance < 5:
			swap = 0
		else:
			swap = 1
		theBudget =int( budgets[i])
		if theBudget < 50:
			theBudget = 50
		elif theBudget > 1000:
			theBudget = 1000
		theBudget = str(theBudget)
		requestDate = "20180731"
		cnct = mariadb.connect(user = 'root', password = '', database = 'fastravel')
		cur = cnct.cursor()
		insertApt = "INSERT INTO Apartments (userid, city_code, swap, start_date, end_date, budget, request_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		print(email)
		#print(city)
		#print(startDate + " " + endDate)
		#print(theBudget)
		#print(swap)
		#print(requestDate)
		#print([insertApt, (str(email), str(city), str(swap), str(startDate), str(endDate), str(theBudget), str(requestDate))])
		cur.execute(insertApt, (str(email), str(city), str(swap), str(startDate), str(endDate), str(theBudget), str(requestDate)))
		cnct.commit()
		cur.close()
		cnct.close()
			
if __name__  =="__main__":
	myGenerator(2)		
		
		

