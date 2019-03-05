from flask import Flask, render_template, redirect, url_for, request
import pymysql
import mysql.connector as mariadb
from flask_mail import Mail, Message
import redis
import rq
import time
import test_task
from passlib.hash import sha256_crypt as sha

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'fastravelout@gmail.com'
app.config['MAIL_PASSWORD'] = 'fastravel1qaz'
app.config['MAIL_DEFAULT_SENDER'] = 'fastravelout@gmail.com'
app.config['MAIL_MAX_EMAILS'] = 100

app.config['REDIS_URL'] = 'redis://'
app.redis = redis.from_url(app.config['REDIS_URL'])
app.task_queue = rq.Queue('emailq', connection = app.redis)
mail = Mail(app)

info = {'user':'', 'data':''}

@app.route('/')
def login():
	msg = 'To register or login, enter an email address with a password.'

	if(info['user'] != ''):
		info['data'] = str(info['user']) + ' logged out. ' + msg
		info['user'] = ''
	else:
		info['data'] = msg

	return render_template('login.html', info = info)

@app.route('/index.html', methods = ['GET', 'POST'])
def index():

	if(info['user'] != ''):
		return render_template('index.html', info = info)

	result = request.form

	email = str(result['email'])
	password = str(result['password'])

	if(email == '' or password == ''):
		info['data'] = 'Email or password left blank, please try again.'
		return render_template('login.html', info = info)

	mariadb_connection = mariadb.connect(user = 'root', password = '', database = 'fastravel')
	cur = mariadb_connection.cursor()
	
	namecheck = "SELECT Login.email FROM Login WHERE Login.email = %s"
	cur.execute(namecheck, (email,))

	names = cur.fetchall()

	if(names == []):
		add = "INSERT INTO Login VALUES (%s, %s)"
		cur.execute(add, (email, sha.encrypt(password)))
		mariadb_connection.commit()
		info['user'] = email
		return render_template('index.html', info = info)
	else:
		passcheck = "SELECT Login.password FROM Login WHERE Login.email = %s"
		cur.execute(passcheck, (email,))
		tuples = cur.fetchall()
		if(sha.verify(password, str(tuples[0][0]))):
			info['user'] = email
			return render_template('index.html', info = info)
		else:
			info['data'] = 'Incorrect password, please try again.'
			return render_template('login.html', info = info)

@app.route('/citiesQuery.html')
def db():
	mariadb_connection = mariadb.connect(user = 'root', password = '', database = "test1")
	cur = mariadb_connection.cursor()
	cur.execute("SELECT * FROM cities GROUP BY name")
	info['data'] = cur.fetchall()
	return render_template('citiesQuery.html', info = info)

@app.route('/addCity.html', methods = ['GET', 'POST'])
def addCity():
	return render_template('addCity.html', info = info)

@app.route('/addCityResult.html', methods = ['POST'])
def result():
	result = request.form
	info['data'] = str(request.form.get('cityName'))
	mariadb_connection = mariadb.connect(user = 'root', password = '', database = 'test1')
	cur = mariadb_connection.cursor()
	cur.execute("INSERT INTO cities (name) VALUES (%s)", (info['data'],))
	mariadb_connection.commit()
	return render_template("addCityResult.html", info = info)

@app.route('/removeCity.html', methods = ['GET','POST'])
def removeCity():
	return render_template('removeCity.html', info = info)

@app.route('/removeCityResult.html', methods = ['GET', 'POST'])
def removeResult():
	result=request.form
	info['data'] = str(request.form.get('cityName'))
	mariadb_connection = mariadb.connect(user = 'root', password = '', database = 'test1')
	cur = mariadb_connection.cursor()
        queryCheck = "SELECT * FROM cities WHERE name = %s"
	queryDelete = "DELETE FROM cities WHERE name = %s"

        cur.execute(queryCheck, (info['data'],))
        row = cur.fetchall()

	if(row == []):
		return render_template("removeCityNotFound.html", info = info)
	else:
		cur.execute(queryDelete, (info['data'],))
		mariadb_connection.commit()
		return render_template("removeCityResult.html", info = info)

@app.route('/flightQuery.html', methods = ['GET', 'POST'])
def flightDateRange():
	return render_template('flightQuery.html', info = info)

@app.route('/flightOut.html', methods = ['GET', 'POST'])
def flightOut():
	mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
	cur = mariadb_connection.cursor()
	result = request.form
	date1 = int(result['startDate'])
	date2 = int(result['endDate'])

	query = "SELECT * FROM Flights WHERE Flights.date >= %s AND Flights.date <= %s"
	cur.execute(query, (date1, date2))
	info['data'] = cur.fetchall()

	return render_template('flightOut.html', info = info)

@app.route('/budgetQuery.html', methods = ['GET', 'POST'])
def budget_query():
        return render_template('budgetQuery.html')

@app.route('/budgetOut.html', methods = ['GET', 'POST'])
def budget_out():
        mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
        cur = mariadb_connection.cursor()
        result = request.form
	origin_city = result['origin_city']
	budget = int(result['budget'])
        date1 = int(result['startDate'])
        date2 = int(result['endDate'])
        query = "SELECT * FROM Flights WHERE Flights.date >= %s AND Flights.date <= %s AND Flights.origin = %s AND Flights.price < %s"
        cur.execute(query, (date1, date2, origin_city, budget))
        data = cur.fetchall()
        return render_template('budgetOut.html', data = data)

@app.route('/advancedQuery.html', methods = ['GET', 'POST'])
def advanced_query():
	return render_template('advancedQuery.html', info = info)

@app.route('/advancedOut2.html', methods = ['GET', 'POST'])
def advanced_out2():
        mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
        cur = mariadb_connection.cursor()
        result = request.form
	origin_city = result['origin_city']
	budget = int(result['budget'])
        ed = int(result['edDate'])
        ld = int(result['ldDate'])
        er = int(result['erDate'])
        lr = int(result['lrDate'])

        query = """ SELECT departure.origin AS origin1, departure.destin AS destin1, departure.date AS date1, departure.price AS price1, 	departure.airline AS airline1,
	 ret.date AS date2,  ret.price AS price2, ret.airline AS airline2 ,ret.price+departure.price AS totalFlightPrice
	FROM Flights AS departure, Flights AS ret 
	WHERE departure.date >= %s AND departure.date <= %s AND ret.date >= %s AND ret.date <= %s and departure.origin = %s AND ret.destin = %s AND departure.destin = ret.origin AND 
	ret.price < %s AND departure.price < %s AND ret.price + departure.price < %s
	ORDER BY totalFlightPrice ASC """	

        cur.execute(query, (ed, ld, er, lr, origin_city, origin_city, budget, budget, budget))
        info['data'] = cur.fetchall()
        return render_template('advancedOut2.html', info = info)


@app.route('/advancedOut.html', methods = ['GET', 'POST'])
def advanced_out():
        mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
        cur = mariadb_connection.cursor()
        result = request.form
        origin_city = result['origin_city']
        budget = int(result['budget'])
        ed = int(result['edDate'])
        ld = int(result['ldDate'])
        er = int(result['erDate'])
        lr = int(result['lrDate'])

        query = """ SELECT totalData.*, AVG(wthr.rating) as averageRating   FROM          (SELECT flightData.* , SUM(mph2.price)  AS totalStayPrice, SUM(mph2.price) + flightData.totalFlightPrice AS totalPrice FROM (SELECT DISTINCT departure.origin AS origin1, departure.destin AS destin1, departure.date AS date1, departure.price AS price1,        departure.airline AS airline1,  ret.date AS date2,  ret.price AS price2, ret.airline AS airline2 ,ret.price+departure.price AS totalFlightPrice FROM Flights AS departure, Flights AS ret ,min_price_hotel as temp  WHERE departure.date >= %s AND departure.date <= %s AND ret.date >= %s AND ret.date <= %s AND departure.origin = %s AND ret.destin = %s AND departure.destin = ret.origin  AND ret.price < %s and departure.price<%s AND departure.price + ret.price < %s AND (SELECT SUM(temp.price) FROM min_price_hotel AS temp WHERE temp.c_code = departure.destin AND temp.date >= departure.date AND temp.date<= ret.date) + departure.price + ret.price < %s) AS flightData, min_price_hotel as mph2  WHERE mph2.c_code = flightData.destin1 AND mph2.date >= flightData.date1 AND mph2.date <= flightData.date2 GROUP BY flightData.date1,flightData.date2,flightData.destin1,flightData.totalFlightPrice) AS totalData, Weather As wthr WHERE wthr.code = totalData.destin1 AND wthr.date >= totalData.date1 AND wthr.date <= totalData.date2 GROUP BY totalData.date1,totalData.date2,totalData.destin1,totalData.totalFlightPrice ORDER BY averageRating DESC """

        cur.execute(query, (ed, ld, er, lr, origin_city, origin_city,budget, budget, budget, budget))
        info['data'] = cur.fetchall()
        return render_template('advancedOut.html', info = info)


@app.route('/updateWeather.html', methods = ['GET', 'POST'])
def updateWeather():
	return render_template('updateWeather.html', info = info)

@app.route('/updateWeatherResult.html', methods = ['GET', 'POST'])
def updateWeatherResult():
	result = request.form
	mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
	cur = mariadb_connection.cursor()
	city = result['cityCode']
	date_start = result['startDate']
	date_end = result['endDate']

	query = "SELECT * FROM Weather WHERE Weather.code = %s AND Weather.date >= %s AND Weather.date <= %s"
	cur.execute(query, (city, date_start, date_end))
	info['data'] = cur.fetchall()
	return render_template("updateWeatherResult.html", info = info)

@app.route('/updateWeatherConfirm.html', methods = ['GET', 'POST'])
def updateWeatherConfirm():
	result = request.form
	key = str(result['recordKey'])
	rating = float(result['newRating'])
	city = key[0:3]
	date = key[4:12]
	time = key[13:]

	query = "UPDATE Weather SET Weather.rating = %s WHERE Weather.code = %s AND Weather.date = %s AND Weather.time = %s"
	mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
	cur = mariadb_connection.cursor()
	cur.execute(query, (rating, city, date, time))
	mariadb_connection.commit()

	query2 = "SELECT * FROM Weather WHERE Weather.code = %s AND Weather.date = %s AND Weather.time = %s"
	cur.execute(query2, (city, date, time))
	info['data'] = cur.fetchall()
	return render_template("updateWeatherConfirm.html", info = info)

@app.route('/addApartment.html', methods = ['GET', 'POST'])
def addApartment():

	mariadb_connection = mariadb.connect(user = 'root', password = '', database = 'fastravel')
	cur = mariadb_connection.cursor()
	
	query = "SELECT * FROM Apartments WHERE Apartments.userid = %s"

	cur.execute(query, (info['user'],))
	tuples = cur.fetchall()

	if(tuples != []):
		info['data'] = 'We already have your apartment listed in our database.'
		return render_template('apartmentResult.html', info = info)

	return render_template('addApartment.html', info = info)

@app.route('/addApartmentResult.html', methods = ['GET', 'POST'])
def addApartmentResult():
	info['data'] = request.form
	mariadb_connection = mariadb.connect(user = 'root', password = '', database = 'fastravel')
	cur = mariadb_connection.cursor()
	query = "INSERT INTO Apartments (userid, city_code, swap, start_date, end_date, budget, request_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"

	cur.execute(query, (str(info['user']), str(info['data']['cityName']), str(info['data']['swap']), str(info['data']['sDate']), str(info['data']['eDate']), str(info['data']['budget']), str(info['data']['reqDate'])))

	mariadb_connection.commit()
	return render_template('addApartmentResult.html', info = info)

@app.route('/updateApartment.html', methods = ['GET', 'POST'])
def updateApartment():

	mariadb_connection = mariadb.connect(user = 'root', password = '', database = 'fastravel')
	cur = mariadb_connection.cursor()
	
	query = "SELECT * FROM Apartments WHERE Apartments.userid = %s"

	cur.execute(query, (info['user'],))
	tuples = cur.fetchall()

	if(tuples == []):
		info['data'] = 'You currently do not have an apartment listed in our database.'
		return render_template('apartmentResult.html', info = info)

	return render_template('updateApartment.html', info = info)

@app.route('/updateApartmentResult.html', methods = ['GET', 'POST'])
def updateApartmentResult():

	result = request.form

	mariadb_connection = mariadb.connect(user = 'root', password = '', database = 'fastravel')
	cur = mariadb_connection.cursor()
	
	query = "SELECT * FROM Apartments WHERE Apartments.userid = %s"

	cur.execute(query, (info['user'],))
	tuples = cur.fetchall()

	if(tuples == []):
		info['data'] = 'You currently do not have an apartment listed in our database.'
	else:
		update = "UPDATE Apartments SET city_code = %s, swap = %s, start_date = %s, end_date = %s, budget = %s, request_date = %s WHERE Apartments.userid = %s"
		values = (str(result['cityName']), str(result['swap']), str(result['sDate']), str(result['eDate']), str(result['budget']), str(result['reqDate']), str(info['user']))

		cur.execute(update, values)
		mariadb_connection.commit()

		aptmailcheck = "SELECT * FROM AptMail WHERE AptMail.userid = %s"
		cur.execute(aptmailcheck, (info['user'],))
		check = cur.fetchall()

		if(check != []):
			update2 = "UPDATE AptMail SET city_code = %s, swap = %s, start_date = %s, end_date = %s, budget = %s, request_date = %s WHERE AptMail.userid = %s"
			cur.execute(update2, values)
			mariadb_connection.commit()

		info['data'] = 'Your apartment has been updated in our database.'

	return render_template('apartmentResult.html', info = info)

@app.route('/removeApartment.html')
def removeApartment():

	mariadb_connection = mariadb.connect(user = 'root', password = '', database = 'fastravel')
	cur = mariadb_connection.cursor()
	
	query = "SELECT * FROM Apartments WHERE Apartments.userid = %s"

	cur.execute(query, (info['user'],))
	tuples = cur.fetchall()

	if(tuples == []):
		info['data'] = 'You currently do not have an apartment listed in our database.'
	else:
		remove = "DELETE FROM Apartments WHERE Apartments.userid = %s"
		cur.execute(remove, (info['user'],))
		mariadb_connection.commit()

		aptmailcheck = "SELECT * FROM AptMail WHERE AptMail.userid = %s"
		cur.execute(aptmailcheck, (info['user'],))
		check = cur.fetchall()

		if(check != []):
			remove = "DELETE FROM AptMail WHERE AptMail.userid = %s"
			cur.execute(remove, (info['user'],))
			mariadb_connection.commit()

		info['data'] = 'Your apartment has been removed from our database.'

	return render_template('apartmentResult.html', info = info)

@app.route('/aptQuery.html')
def queryApt():
	return render_template('aptQuery.html', info = info)

@app.route('/aptOut.html', methods = ['GET', 'POST'])
def apartment_out_dep():
        mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
        cur = mariadb_connection.cursor()
        result = request.form
	origin_city = str(result['origin_city'])
	budget = int(result['budget'])
        ed = int(result['edDate'])
        ld = int(result['ldDate'])
        er = int(result['erDate'])
        lr = int(result['lrDate'])

        query = """ SELECT departure.origin AS origin1, departure.destin AS destin1, departure.date AS date1, departure.price AS price1, 	departure.airline AS airline1,
	 ret.date AS date2,  ret.price AS price2, ret.airline AS airline2 ,ret.price+departure.price AS totalFlightPrice
	FROM Flights AS departure, Flights AS ret, Apartments as apt
	WHERE apt.swap = 1 AND apt.start_date >= %s AND apt.start_date <= %s AND apt.end_date >= %s AND apt.end_date <= %s AND departure.date = apt.start_date AND ret.date = apt.end_date AND departure.destin = apt.city_code AND departure.origin = %s AND ret.destin = %s AND departure.destin = ret.origin AND 

	ret.price < %s AND departure.price < %s AND ret.price + departure.price < %s
	ORDER BY totalFlightPrice ASC """	

        cur.execute(query, (ed, ld, er, lr, origin_city, origin_city, budget, budget, budget))
        info['data'] = cur.fetchall()
        return render_template('aptOut.html', info = info)

@app.route('/doubleOut.html', methods = ['GET', 'POST'])
def double_out():
        mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
        cur = mariadb_connection.cursor()
	userid = str(info['user'])

        query = """ SELECT apt_swap.*, AVG(wthr.rating) as weatherAvg FROM (SELECT seaRes.userid AS otheruser, departure.origin AS origin1, departure.destin AS destin1, departure.date AS date1, departure.price AS price1, 	departure.airline AS airline1,
	 ret.date AS date2,  ret.price AS price2, ret.airline AS airline2 ,ret.price+departure.price AS totalFlightPrice
	FROM Flights AS departure, Flights AS ret, Flights AS oD, Flights AS oRe, Apartments as searcher, Apartments as seaRes
	WHERE %s = searcher.userid AND seaRes.swap = 1 AND searcher.swap = 1 AND  departure.destin = seaRes.city_code AND departure.origin = searcher.city_code AND ret.destin = searcher.city_code AND searcher.end_date > seaRes.start_date AND searcher.start_date < seaRes.end_date AND departure.destin = ret.origin AND ((departure.date = searcher.start_date AND searcher.start_date >= seaRes.start_date) OR (departure.date = seaRes.start_date AND seaRes.start_date >= searcher.start_date)) AND ((ret.date = searcher.end_date AND searcher.end_date <= seaRes.end_date) OR (ret.date = seaRes.end_date AND seaRes.end_date <= searcher.end_date)) AND ret.price < searcher.budget AND departure.price < searcher.budget AND ret.price + departure.price < searcher.budget AND oD.destin = departure.origin AND oD.origin = departure.destin and oD.date = departure.date AND oRe.destin = oD.origin AND oRe.origin = oD.destin AND oRe.date = ret.date AND oRe.price + oD.price < seaRes.budget
	ORDER BY totalFlightPrice ASC) AS apt_swap, Weather as wthr WHERE wthr.code = destin1 AND wthr.date >= apt_swap.date1 AND wthr.date <= apt_swap.date2 GROUP BY
otheruser ORDER BY weatherAvg DESC"""	

        cur.execute(query, (userid,))
        info['data'] = cur.fetchall()
	#print(info)
        return render_template('doubleOut.html', info = info)

@app.route('/mailerTest.html')
def email_test():
	job = app.task_queue.enqueue('test_task.example', 23)
	return render_template('phpinfo.php')
@app.route('/phpinfo.php')
def phpinfo():
	return render_template('phpinfo.php')
def example(seconds):
	print('init')
	for i in range(seconds):
		print(i)
		time.sleep(1)
	print('done')
if __name__ == '__main__':
	app.debug = True
	app.run(host = "172.22.146.2", port = 8000)
