import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import sklearn
from sklearn.cluster import KMeans
import datetime



# columns=['user_id', 'total_purchases', 'total_expense', 'average_expense', 'last_purchase']

def create_user_intel(thegroup: tuple) -> list:
	result = []
	basket = thegroup[1].groupby(thegroup[1][2])[3]

	result.append(thegroup[0])				# user_id
	result.append(basket.ngroups)			# total_purchases
	result.append(thegroup[1][3].sum())		# total_expense

	reduced_basket = [x[1].sum() for x in basket]
	total_basket = sum(reduced_basket) / len(reduced_basket)

	result.append(total_basket)				# average_expense
	# print("###", type(thegroup[1][0].iloc[0]), thegroup[1][0].iloc[0])
	result.append((datetime.datetime(2023, 3, 1, tzinfo=None) -  thegroup[1][0].iloc[0].to_pydatetime().replace(tzinfo=None)).total_seconds())			# last_purchase

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

	used_data = pd.DataFrame({'recency': user_total_expense['last_purchase'], 'frequency': user_total_expense['total_purchases']})

	print(used_data)

	print("---------- 4 ----------")
	distorsions = []
	for k in range(2, 20):
		kmeans = KMeans(n_clusters=k)
		kmeans.fit(used_data)
		distorsions.append(kmeans.inertia_)

	plt.figure(200)
	plt.plot(range(2, 20), distorsions)
	plt.grid(True)


	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)







if __name__ == '__main__':
    main()

