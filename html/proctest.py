import pymysql
import mysql.connector as mariadb
import redis
import rq
from itertools import chain
import time
def double_out(inEmail):
		mariadb_connection = mariadb.connect(user = 'root', password = '', database = "fastravel")
		cur = mariadb_connection.cursor()	
		#query = "call apartment_query(%s)"
		#cur.execute(query,(inEmail,))
		result = cur.callproc('apartment_query', (inEmail,))
		exist = cur.stored_results()
		for x in exist:
			out = x.fetchall()
			print("/n")
		print(out)
		cur.close()
		mariadb_connection.close()
if __name__ == "__main__":
	double_out('12EJftPJ4k2azONvkvbF@fakefake.com')
