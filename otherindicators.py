import ccxt
import mysql.connector

import os
import sys
import time
import logging
import telegram
import statistics




#TOKEN = "688361182:AAGJTUu6PV4mjcKlSgtyZ52w-8B-uwJBUS0"
#URL = "https://api.telegram.org/bot{}/".format(TOKEN)



cnx = mysql.connector.connect(user='root', password='Mumina12!23',
							  host='localhost', database='coinbuys',
							  auth_plugin='mysql_native_password')

mycursor = cnx.cursor()

old_database_coin_scores ={}

#sql = """SELECT * FROM coinscores """
mycursor.execute("SELECT * FROM coinscores WHERE datetimeofinsert > DATE_SUB(NOW(), INTERVAL 13 MINUTE)")
myresult = mycursor.fetchall()
cnx.commit()
for row in myresult:
	coin_score_symbol = row[1]
	coin_score_database_value = row[2]
	old_database_coin_scores[coin_score_symbol] = coin_score_database_value
	print (coin_score_symbol)
	print (coin_score_database_value)



bittrex = ccxt.bittrex({
	'enableRateLimit': True,  # this option enables the built-in rate limiter
	})

markets = bittrex.load_markets()

#for x in old_database_coin_scores:
#    time.sleep (bittrex.rateLimit / 1000) # time.sleep wants seconds
#    print (x, bittrex.fetch_ohlcv (x, '1d')) # one day


