from app import app
from flask import Flask, render_template, redirect, url_for, request, current_app
import pymysql
import mysql.connector as mariadb
from flask_mail import Mail, Message
import redis
import rq
from itertools import chain
import time
def double_out():
	while(True):
		mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
		cur = mariadb_connection.cursor()

		outQ = """SELECT userid FROM AptMail"""
		cur.execute(outQ, )
		users = cur.fetchall()
		#print(cities)
		for user in users:
			print(user)
			print(user[0])	
		#result = request.form
		#userid = result['userid']
			cur.callproc('apartment_query', (str(user[0]),))
			exist = cur.stored_results()
			for x in exist:
				data = x.fetchall()
			with app.app_context():
				mail = Mail(app)
				with mail.connect() as conn:
					for results in data:
						email = results[0]
						msg = Message("Match found with " + user[0], recipients = [str(results[0]), "fastravelout@gmail.com"])
						outStr = "Email: " + user[0] + "\nDestination: " + results[1] + "\n\nDeparture Date: " + str(results[3]) + "\nDeparture Flight Price: " + str(results[4]) + "\nDeparture Airline: " + results[5] + "\n\nReturn Date: " + str(results[6]) + "\nReturn Flight Price: " + str(results[7]) + "\nReturn Airline: " + results[8] + "\nTotal Price: " + str(results[9]) +"\nWeather: " + str(results[10]) +  "\n\nPlease contact " + user[0] + " to confirm"
						msg.body = outStr
						mail = Mail(app)
						conn.send(msg)
			
			query = "SELECT * FROM AptMail where userid = %s"
			cur.execute(query,(user[0],))
			exist = cur.fetchall()
			if(cur.fetchall != []):
				query = """delete from AptMail where userid = %s"""
				cur.execute(query, (user[0],))
				mariadb_connection.commit()
		cur.close()
		mariadb_connection.close()
		time.sleep(60)
		 #       return render_template('doubleOut.html', data = data)
if __name__ == "__main__":
	double_out()
