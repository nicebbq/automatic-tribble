from app import app
from flask import Flask, render_template, redirect, url_for, request, current_app
import pymysql
import mysql.connector as mariadb
from flask_mail import Mail, Message
import redis
import rq
from itertools import chain

def double_out():
        mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
        cur = mariadb_connection.cursor()

	outQ = """SELECT userid FROM Apartments"""
	cur.execute(outQ, )
	userids = cur.fetchall()
	for users in userids:
		print(users)
		print(users[0])	
        #result = request.form
	#userid = result['userid']

		query = """ SELECT seaRes.userid, departure.origin AS origin1, departure.destin AS destin1, departure.date AS date1, departure.price AS price1, 	departure.airline AS airline1,
		 ret.date AS date2,  ret.price AS price2, ret.airline AS airline2 ,ret.price+departure.price AS totalFlightPrice
		FROM Flights AS departure, Flights AS ret, Flights AS oD, Flights AS oRe, Apartments as searcher, Apartments as seaRes
		WHERE %s = searcher.userid AND seaRes.swap = 1 AND searcher.swap = 1 AND  departure.destin = seaRes.city_code AND departure.origin = searcher.city_code AND ret.destin = searcher.city_code AND searcher.end_date > seaRes.start_date AND searcher.start_date < seaRes.end_date AND departure.destin = ret.origin AND ((departure.date = searcher.start_date AND searcher.start_date >= seaRes.start_date) OR (departure.date = seaRes.start_date AND seaRes.start_date >= searcher.start_date)) AND ((ret.date = searcher.end_date AND searcher.end_date <= seaRes.end_date) OR (ret.date = seaRes.end_date AND seaRes.end_date <= searcher.end_date)) AND ret.price < searcher.budget AND departure.price < searcher.budget AND ret.price + departure.price < searcher.budget AND oD.destin = departure.origin AND oD.origin = departure.destin and oD.date = departure.date AND oRe.destin = oD.origin AND oRe.origin = oD.destin AND oRe.date = ret.date AND oRe.price + oD.price < seaRes.budget
		ORDER BY totalFlightPrice ASC """	
		cur.execute(query, (str(users[0]),))
		data = cur.fetchall()
		with app.app_context():
			msg = Message("Test", recipients = ["fastravelout@gmail.com"])
			msg.body = str(list(chain.from_iterable(data)))
			mail = Mail(app)
			mail.send(msg)
	 #       return render_template('doubleOut.html', data = data)
