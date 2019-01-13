import ccxt
import mysql.connector

import os
import sys
import time
import logging
import telegram
from collections import Counter



cnx = mysql.connector.connect(user='root', password='Mumina12!23',
							  host='localhost', database='coinbuys',
							  auth_plugin='mysql_native_password')

mycursor = cnx.cursor()

coinscores_dict = {}
sentiment_dict = {}
final_scores_dict = {}

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



for x in coinscores_dict.keys():
    first_word = x.split('/')[0]  # split on whitespace, take the first result
    if first_word in sentiment_dict:
        loop_score = sentiment_dict.get(first_word)
        coin_indvidual_score = coinscores_dict.get(x)
        final_score = float(coin_indvidual_score) + float(loop_score)
        final_scores_dict[x] = final_score


data_sorted = {k: v for k, v in sorted(final_scores_dict.items(), key=lambda x: x[1])}
print(data_sorted)
