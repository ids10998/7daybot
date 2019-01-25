import requests 
import json 
from datetime import date, timedelta
import ccxt
import time
import mysql.connector

cnx = mysql.connector.connect(user='root', password='Mumina12!23',
							  host='localhost', database='coinbuys',
							  auth_plugin='mysql_native_password')

mycursor = cnx.cursor()


bittrex = ccxt.bittrex({
	'enableRateLimit': True,  # this option enables the built-in rate limiter
	})

markets = bittrex.load_markets()
whichmarket = (bittrex.symbols)

yesterday_date = str(date.today() - timedelta(1))
today_date = str(date.today() + timedelta(1))

coin_senntiment = {}

f = 0
y = 0

coins_to_analyse = []

while y < len(whichmarket):
	coin = whichmarket[y]
	sep = '/'
	coin = coin.split(sep, 1)[0]
	coins_to_analyse.append(coin)
	y = y + 1


coins_to_analyse = list(dict.fromkeys(coins_to_analyse))

while f < len(coins_to_analyse):
	try:
		coin = coins_to_analyse[f]
		print (coin)
		url = 'https://www.bittsanalytics.com/bittsanalytics/api.php/sentiment?filter[]=datum,bt,' + str(yesterday_date) + ',' + str(today_date) + '&filter[]=valuta,eq,' + str(coin)
		r = requests.get(url, headers={"x-api-key":"b4dcde2ce5fb2d0b887b5eb6f0cdd449"}).json()
		print (r)
		sentiment = r["sentiment"]["records"][0][2]

		if sentiment != "":
			sql = "INSERT INTO sentiment (symbol, datetimeofalert, score) VALUES (%s, NOW(), %s)"
			val = [
				(coin, sentiment)
				]

			mycursor.executemany(sql, val)

			cnx.commit()

			print(mycursor.rowcount, "was inserted.")

		print (sentiment)
		time.sleep(1)
		f = f + 1

	except (IndexError, KeyError) as error:
		print(error) # might log or have some other default behavior...
		time.sleep(1)
		f = f + 1
		continue 
	

