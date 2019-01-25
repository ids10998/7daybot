import ccxt
import mysql.connector

import os
import sys
import time
import logging
import telegram
from collections import Counter
from heapq import nlargest



cnx = mysql.connector.connect(user='root', password='Mumina12!23',
							  host='localhost', database='coinbuys',
							  auth_plugin='mysql_native_password')

mycursor = cnx.cursor()

coinscores_dict = {}
sentiment_dict = {}
final_scores_dict = {}
creepingcoinscores_list =[]
final_creepingcoinscores_list = []
sql = """SELECT * FROM coinscores WHERE datetimeofinsert > DATE_SUB(NOW(), INTERVAL 13 MINUTE)"""
mycursor.execute(sql)
myresult = mycursor.fetchall()
for row in myresult:

	coin_score_symbol = row[1]
	coin_score_database_value = row[2]
	print(row[0])
	print (coin_score_symbol)
	print (coin_score_database_value)
	coinscores_dict[coin_score_symbol] = coin_score_database_value


sql = """SELECT * FROM sentiment WHERE datetimeofalert >= CURDATE() """
mycursor.execute(sql)
myresult = mycursor.fetchall()
for row in myresult:

	sentiment_coin = row[1]
	sentiment_score = row[3]

	sentiment_dict[sentiment_coin] = sentiment_score


sql = """SELECT * FROM creepingcoinscores WHERE datetimeofinsert > DATE_SUB(NOW(), INTERVAL 12 HOUR) """
mycursor.execute(sql)
myresult = mycursor.fetchall()
for row in myresult:
	creeping_coin_score_symbol = row[1]
	creepingcoinscores_list.append(creeping_coin_score_symbol)

for i in creepingcoinscores_list:
  if i not in final_creepingcoinscores_list:
    final_creepingcoinscores_list.append(i)

print (final_creepingcoinscores_list)

for x in coinscores_dict.keys():
    first_word = x.split('/')[0]  # split on whitespace, take the first result
    if first_word in sentiment_dict:
        loop_score = sentiment_dict.get(first_word)
        coin_indvidual_score = coinscores_dict.get(x)
        final_score = float(coin_indvidual_score) + float(loop_score)
        final_scores_dict[x] = final_score


for x in final_scores_dict.keys():
	if x in final_creepingcoinscores_list:
		current_score = final_scores_dict.get(x)
		calculation_scores = float(current_score) + 0.5
		final_scores_dict[x] = calculation_scores


data_sorted = {k: v for k, v in sorted(final_scores_dict.items(), key=lambda x: x[1])}
print(data_sorted)


#bot = telegram.Bot('796174401:AAFg0imveWhaQMykjB6Y8C4R9Fw-nvm4gMw')

#twenty_largest = nlargest(20, data_sorted, key=data_sorted.get)
#print(twenty_largest)

#new_list = []
#for x in twenty_largest:
#	coin_ticker = x.split('/')[0]
#	new_list.append(coin_ticker)

#set(new_list)
#print (new_list)	



#chat_id = bot.get_updates()[-1].message.chat_id
#bot.send_message(chat_id=chat_id, text='🐂 <b>Hourly Coins</b>\n' + str(last_item) + '\n' + str(second_last_item) + '\n' + str(third_last_item) + '\n' + str(fourth_last_item) + '\n' + str(fifth_last_item), parse_mode=telegram.ParseMode.HTML)



#print (length_of_dict)















