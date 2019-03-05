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
		mariadb_connection = mariadb.connect(user = 'root', password = '', database = "test1")
		cur = mariadb_connection.cursor()

		outQ = """SELECT * FROM trig_test"""
		cur.execute(outQ, )
		cities = cur.fetchall()
		print(cities)
		for city in cities:
			print(city)
			print(city[0])	
		#result = request.form
		#userid = result['userid']

			
			with app.app_context():
				msg = Message("Test", recipients = ["fastravelout@gmail.com"])
				msg.body = str(city[0]) + "Added"
				mail = Mail(app)
				mail.send(msg)
			query = """delete from trig_test where city = %s"""
			cur.execute(query, (city[0],))
			mariadb_connection.commit()
		cur.close()
		mariadb_connection.close()
		time.sleep(60)
		 #       return render_template('doubleOut.html', data = data)
if __name__ == "__main__":
	double_out()
