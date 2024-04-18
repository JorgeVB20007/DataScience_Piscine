import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import sklearn




# columns=['user_id', 'total_purchases', 'total_expense', 'average_expense', 'last_purchase']

def create_user_intel(thegroup: tuple) -> list:
	result = []
	result.append(thegroup[0])				# user_id
	result.append(len(thegroup[1].index))	# total_purchases
	result.append(thegroup[1][3].sum())		# total_expense

	basket = thegroup[1].groupby(thegroup[1][2])
	reduced_basket = [x.sum() for x in basket]
	total_basket = reduced_basket.mean()

	result.append(total_basket)				# average_expense
	result.append(thegroup[1][0])			# last_purchase

	return result





def main():
	load_dotenv()

	print("Connecting to DB...")
	conn = psycopg2.connect(
		host = 'localhost',
		dbname = os.getenv('DB_NAME'),
		user = os.getenv('DB_USER'),
		password = os.getenv('DB_PASSWORD'),
		port = os.getenv('DB_PORT')
	)

	try:
		cur = conn.cursor()
	except Exception as msg:
		print(msg)
		return
	
	print("Creating temp table...")
	cur.execute("""CREATE TABLE IF NOT EXISTS purchasers (
	event_time TIMESTAMPTZ,
	user_id BIGINT,
	user_session UUID,
	price FLOAT
	);
	TRUNCATE purchasers;
	INSERT INTO purchasers(event_time, user_id, user_session, price)
	SELECT event_time, user_id, user_session, price FROM customers WHERE "event_type" = 'purchase' ORDER BY event_time;""")

	print("Getting data from DB...")
	cur.execute("""SELECT * FROM purchasers;""")
	rawtable = pd.DataFrame(cur.fetchall())

	print("---------- 0 ----------")
	print(rawtable)
	print("---------- 1 ----------")

	grouped_by_user = rawtable.groupby(rawtable[1])
	# for x in grouped_by_user:
	# 	print(type(x[1]), x)
	print(grouped_by_user)
	print("---------- 2 ----------")
	
	user_total_expense = pd.DataFrame([create_user_intel(x) for x in grouped_by_user], columns=['user_id', 'total_purchases', 'total_expense', 'average_expense', 'last_purchase'])

	print(user_total_expense)
	print("---------- 3 ----------")


#	Create tables:
	#	user_total_expense
	#	user_average_expense
	#	user_number_of_purchases
	#	user_last_purchase

	print("Loading results...")







if __name__ == '__main__':
    main()

