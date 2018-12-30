import ccxt
import mysql.connector

import os
import sys
import time
import logging
import telegram




#TOKEN = "688361182:AAGJTUu6PV4mjcKlSgtyZ52w-8B-uwJBUS0"
#URL = "https://api.telegram.org/bot{}/".format(TOKEN)



cnx = mysql.connector.connect(user='root', password='Mumina12!23',
							  host='localhost', database='coinbuys',
							  auth_plugin='mysql_native_password')

mycursor = cnx.cursor()

old_database_coin_scores ={}

#sql = """SELECT * FROM coinscores """
mycursor.execute("SELECT * FROM coinscores")
myresult = mycursor.fetchall()
cnx.commit()
for row in myresult:
	coin_score_symbol = row[1]
	coin_score_database_value = row[2]
	old_database_coin_scores[coin_score_symbol] = coin_score_database_value
	print (coin_score_symbol)
	print (coin_score_database_value)

mycursor.execute("TRUNCATE TABLE BUYWALLDATA3")
mycursor.execute("TRUNCATE TABLE coinscores")


bittrex = ccxt.bittrex({
	'enableRateLimit': True,  # this option enables the built-in rate limiter
	})

markets = bittrex.load_markets()
whichmarket = (bittrex.symbols)
list_to_remove = ["BTC/USD","ETH/USDT","XRP/USDT","XRP/BTC","LTC/BTC","BTC/USDT","ETH/BTC","TUSD/BTC","ETH/USD"]
whichmarket= list(set(whichmarket).difference(set(list_to_remove)))
limit = '4%'
f = 0
coins_with_buy_walls = {}
size_of_above_average_buy_order = {}





while f < len(whichmarket):
	try:
		orderbook = ccxt.bittrex().fetch_order_book(whichmarket[f], limit)
		ticker_info = bittrex.fetch_ticker(whichmarket[f]) # ticker for a random symbol
		last_price = ticker_info.get('last')
		volume = ticker_info.get('quoteVolume')
		percentage_change = ticker_info.get('percentage')

		bids = (orderbook['bids'])
		i = 0
		g = 0
		above_average_count = 0
		sum_bids = []
		while i < len(bids):
			var_element = (bids[i])
			sum_array = var_element[0] * var_element[1]
			i = i + 1
			sum_bids.append(sum_array)

		total_bids = sum(sum_bids)	
		if total_bids == 0:
			total_bids = 1
		length_sum_bids = len(sum_bids)
		if length_sum_bids == 0:
			length_sum_bids =1


		average_bid = total_bids / length_sum_bids

		#if an order is 10 times larger than the average bid 
		threshhold = average_bid * 10

		#check to see any above average buy orders 
		while g < len(bids):
			var_element_check = (bids[g])
			sum_array_check = var_element_check[0] * var_element_check[1]
			if volume == 0:
				volume = 1
			volume_threshold = sum_array_check / volume
			#number below is total order size divded by total volume and if its below 0.037 it should be a large order 
			if sum_array_check > threshhold and volume_threshold < 0.037 and percentage_change < 10:

				#find average order price and size of buywall



				#insert order into database

				sql = "INSERT INTO BUYWALLDATA3 (COINPAIR, BUYWALLPRICE, BUYWALLSIZEINBTC, volumethreshold) VALUES (%s, %s, %s, %s)"
				val = [
					(whichmarket[f], var_element_check[0], sum_array_check, volume_threshold)
					]

				mycursor.executemany(sql, val)

				cnx.commit()

				print(mycursor.rowcount, "was inserted.")

				
				above_average_count = above_average_count + 1


			g = g + 1
			

		
		if above_average_count >= 1:
			coins_with_buy_walls[whichmarket[f]] = above_average_count


		
		print ("The coin is:",whichmarket[f])
		print ("There are",above_average_count,"buy walls")
		f = f + 1
	except (ccxt.ExchangeError,ccxt.NetworkError,ccxt.RequestTimeout) as error:
		print('Got an error', type(error).__name__, error.args)
	time.sleep(0.5)
	continue           	

print (coins_with_buy_walls)

#coin_score = {}
#for x in coins_with_buy_walls:
#	if coins_with_buy_walls[x] >= 5:
#		coin_score[x] = 1
#	elif 5 > coins_with_buy_walls[x] > 2:
#		coin_score[x] = 0.75
#	else:
#		coin_score[x] = 0.3

#coin score should rank the size of the buy order not quantity	

#coin_score = {}
#for x in size_of_above_average_buy_order:
#	if size_of_above_average_buy_order[x] <= 0.02:
#		coin_score[x] = 1
#	elif 0.03 >= size_of_above_average_buy_order[x] > 0.02:
#		coin_score[x] = 0.75
#	else:
#		coin_score[x] = 0.3

f = 0
volume_calculation = 0
keys = list(coins_with_buy_walls.keys())
coin_score = {}
#print(coin_score)				
for key in coins_with_buy_walls.keys():
	sql = """SELECT * FROM BUYWALLDATA3 WHERE COINPAIR = '%s' """ % (key)
	rows = 0
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	for row in myresult:
		rows = rows + 1
		id_table = row[0]
		ticker = row[1]
		coin_price = row[2]
		size_order = row[3]
		volume_calculation = row[4]
		volume_calculation = row[4] + volume_calculation

	if rows == 0:
		rows = 1	

	volume_calculation = volume_calculation / rows
	print(volume_calculation)

	if volume_calculation <= 0.02:
		coin_score[key] = 1
	elif 0.03 >= volume_calculation > 0.02:
		coin_score[key] = 0.75
	else:
		coin_score[key] = 0.3

	f = f + 1
	volume_calculation = 0
	rows = 0



#add to an array 
for x in whichmarket:
	if x in coin_score:
		print ("Already in dict")
	else:
		coin_score[x] = 0

print (coin_score)

#old_database_coin_scores = {}
#for key in coins_with_buy_walls.keys():
#	sql = """SELECT * FROM coinscores WHERE symbol = '%s' """ % (key)
#	mycursor.execute(sql)
#	myresult = mycursor.fetchall()
#	coin_score_symbol = row[1]
#	coin_score_database_value = row[2]
#	old_database_coin_scores[key] = coin_score_database_value

#for key in old_database_coin_scores.keys():
#	if old_database_coin_scores[key] == 0 


#print (old_database_coin_scores)

#for key1 in coin_score.keys():
#	sql2 = """SELECT * FROM coinscores WHERE symbol = '%s' """ % (key1)
#	mycursor.execute(sql2)
#	myresult3 = mycursor.fetchall()
#	for row in myresult3:
#		old_coin_score_symbol = row[0]
#		old_coin_score_database_value = row[1]
#		print (old_coin_score_symbol)
#		print (old_coin_score_database_value)
#		old_database_coin_scores[key1] = old_coin_score_database_value

bot = telegram.Bot('688361182:AAGJTUu6PV4mjcKlSgtyZ52w-8B-uwJBUS0')
print(old_database_coin_scores)

for x in old_database_coin_scores:
	new_coin_score = coin_score.get(x)
	if new_coin_score == 1:
		how_big = "Large"
	else:
		how_big = "Medium"

	if float(old_database_coin_scores[x]) < 0.4 and float(new_coin_score) > 0.74:
		ticker_info = bittrex.fetch_ticker(x) # ticker for a random symbol
		last_price = ticker_info.get('last')
		last_price = round(last_price, 2)
		volume = ticker_info.get('quoteVolume')
		percentage_change = ticker_info.get('percentage')
		percentage_change = round(percentage_change, 2)
		print("Alert")
		chat_id = bot.get_updates()[-1].message.chat_id
		bot.send_message(chat_id=chat_id, text='🐂 <b>' + str(x) + '</b>\nBittrex\nSignificant buy wall(s) has appeared\nCurrent buy wall size is: <b>' + str(how_big) + '</b>\nPercentage change: ' + str(percentage_change) +'\nLast price: ' + str(last_price), parse_mode=telegram.ParseMode.HTML)


	
	
		


	


keys1 = list(coin_score.keys())

for a in coin_score:
	coin_final_score = coin_score[a]
	sql5 = "INSERT INTO coinscores (symbol, score) VALUES (%s, %s)"				
	val5 = [(a, coin_final_score)]
	mycursor.executemany(sql5, val5)
	cnx.commit()
	print(mycursor.rowcount, "was inserted.")
	#if old_database_coin_scores.get(key, "") == "":
	#	print ("New coin notification")





#def get_url(url):
#		    response = requests.get(url)
#		    content = response.content.decode("utf8")
#		    return content
#
#
#		def get_json_from_url(url):
#		    content = get_url(url)
#		    js = json.loads(content)
#		    return js
#
#
#		def get_updates():
#		    url = URL + "getUpdates"
#		    js = get_json_from_url(url)
#		    return js
#
#
#		def get_last_chat_id_and_text(updates):
#		    num_updates = len(updates["result"])
#		    last_update = num_updates - 1
#		    text = a
#		    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
#		    return (text, chat_id)
#
#
#		def send_message(text, chat_id):
#		    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
#		    get_url(url)
#		
#		text, chat = get_last_chat_id_and_text(get_updates())
#		send_message(text, chat)
#
#for x in coin_score:
#	text, chat = get_last_chat_id_and_text(get_updates())
#	send_message(text, chat)



