import mysql.connector
import ccxt
import numpy as np


bittrex = ccxt.bittrex({
	'enableRateLimit': True,  # this option enables the built-in rate limiter
	})

markets = bittrex.load_markets()
whichmarket = (bittrex.symbols)

cnx = mysql.connector.connect(user='root', password='Mumina12!23',
							  host='localhost', database='coinbuys',
							  auth_plugin='mysql_native_password')

mycursor = cnx.cursor()

coin_pairs_start = [] 

#get a list of coins that have buy walls


sql1 = """SELECT * FROM BUYWALLDATA3 """
mycursor.execute(sql1)
myresult = mycursor.fetchall()
for row in myresult:
	coin_pairs_start.append(row[1])


coin_pairs = list(set(coin_pairs_start))

#define a few things
avg_coin_price = {}
coin_pairs_ticker = []
f=0
count_row = 0
avg_price_start = 0
avg_price = 0
price = 0
#avg_price_start =[]

while f < len(coin_pairs):
	sql = """SELECT * FROM BUYWALLDATA3 WHERE COINPAIR = '%s' """ % (coin_pairs[f])
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	for row in myresult:
		price=row[2]
		total=row[3]
		avg_price_start = avg_price_start + float(row[2])
		count_row = count_row + 1
		avg_price = avg_price_start / count_row
		#avg_price_start.append(row[2])
		#for c in avg_price_start:
		#	print (avg_price_start)

	coin_pairs_ticker.append(coin_pairs_ticker)    
	print(coin_pairs[f])
	print ('avergae price: ',avg_price)    
	avg_coin_price[coin_pairs[f]]=avg_price

	count_row = 0    
	avg_price_start = 0
	f = f +1    

print(avg_coin_price)

#coin_pairs_ticker = list(set(coin_pairs_ticker))


limit = '10%'
f = 0
coins_with_buy_walls = {}
coins_with_creeping_buy_walls =[]

while f < len(coin_pairs):
	orderbook = ccxt.bittrex().fetch_order_book(coin_pairs[f], limit)
	ticker_info = bittrex.fetch_ticker(coin_pairs[f])
	last_price = ticker_info.get('last')
	volume = ticker_info.get('quoteVolume')

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
		volume_threshold = sum_array_check / volume
		#number below is total order size divded by total volume and if its below 0.037 it should be a large order 
		if sum_array_check > threshhold and volume_threshold < 0.037:

			#check if theres creeping buy orders 
			in_key_avg_price = avg_coin_price.get(coin_pairs[f])
			# the value 1.03 is 3% above the last buy order price 
			if (var_element_check[0] * 1.03) > in_key_avg_price:

				print("Creeping Buy order present")
				print(coin_pairs[f])
				coins_with_creeping_buy_walls.append(coin_pairs[f])

			

		




			above_average_count = above_average_count + 1

		g = g + 1

	
	if above_average_count >= 1:
		coins_with_buy_walls[coin_pairs[f]] = above_average_count


	
	print ("The coin is;",coin_pairs[f])
	print ("There are",above_average_count,"buy walls")
	print (total_bids,"is the sum of orders")
	print ("The average bid is",average_bid)
	f = f + 1

coins_with_creeping_buy_walls = list(set(coins_with_creeping_buy_walls))

print (coins_with_creeping_buy_walls)	














