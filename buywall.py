import ccxt
import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost', database='coinbuys',
                              auth_plugin='mysql_native_password')

mycursor = cnx.cursor()

bittrex = ccxt.bittrex({
	'enableRateLimit': True,  # this option enables the built-in rate limiter
	})

markets = bittrex.load_markets()
whichmarket = (bittrex.symbols)
limit = '10%'
f = 0
coins_with_buy_walls = {}

while f < len(whichmarket):
	orderbook = ccxt.bittrex().fetch_order_book(whichmarket[f], limit)
	ticker_info = bittrex.fetch_ticker(whichmarket[f]) # ticker for a random symbol
	last_price = ticker_info.get('last')
	volume = ticker_info.get('quoteVolume')
	print(volume)
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

			#find average order price and size of buywall



			#insert order into database

			sql = "INSERT INTO BUYWALLDATA3 (COINPAIR, BUYWALLPRICE, BUYWALLSIZEINBTC) VALUES (%s, %s, %s)"
			val = [
  				(whichmarket[f], var_element_check[0], sum_array_check)
				]

			mycursor.executemany(sql, val)

			cnx.commit()

			print(mycursor.rowcount, "was inserted.")




			above_average_count = above_average_count + 1

		g = g + 1

	
	if above_average_count >= 1:
		coins_with_buy_walls[whichmarket[f]] = above_average_count


	
	print ("The coin is;",whichmarket[f])
	print ("There are",above_average_count,"buy walls")
	print (total_bids,"is the sum of orders")
	print ("The average bid is",average_bid)
	f = f + 1

print (coins_with_buy_walls)

coin_score = {}
for x in coins_with_buy_walls:
	if coins_with_buy_walls[x] >= 5:
		coin_score[x] = 1
	elif 5 > coins_with_buy_walls[x] > 2:
		coin_score[x] = 0.75
	else:
		coin_score[x] = 0.3

print(coin_score)				



