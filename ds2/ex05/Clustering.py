import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import sklearn
from sklearn.cluster import KMeans
import datetime
import numpy as np



# columns=['user_id', 'total_purchases', 'total_expense', 'average_expense', 'last_purchase']

def create_user_intel(thegroup: tuple) -> list:
	result = []
	basket = thegroup[1].groupby(thegroup[1][2])[3]

	result.append(thegroup[0])				#? user_id
	result.append(basket.ngroups)			#? total_purchases
	result.append(thegroup[1][3].sum())		#? total_expense

	reduced_basket = [x[1].sum() for x in basket]
	total_basket = sum(reduced_basket) / len(reduced_basket)

	result.append(total_basket)				#? average_expense

	result.append(thegroup[1][0].iloc[0])	#? last_purchase
	result.append((datetime.datetime(2023, 3, 1, tzinfo=None) -  thegroup[1][0].iloc[0].to_pydatetime().replace(tzinfo=None)).total_seconds())	# last_purchase_seconds

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

	grouped_by_user = rawtable.groupby(rawtable[1])

	
	user_total_expense = pd.DataFrame([create_user_intel(x) for x in grouped_by_user], columns=['user_id', 'total_purchases', 'total_expense', 'average_expense', 'last_purchase', 'last_purchase_seconds'])


	used_data = pd.DataFrame({'last_purchase_seconds': user_total_expense['last_purchase_seconds'], 'total_purchases': user_total_expense['total_purchases']})


	kmeans = KMeans(n_clusters=4)
	kmeans.fit(used_data)
	labels = kmeans.labels_
	y_means = kmeans.predict(used_data)


	used_data['clusters'] = labels
	used_data['average_expense'] = user_total_expense['total_expense']

	allclusters = used_data.groupby('clusters')

	lst_purch = []
	tot_purch = []
	avg_purch = []
	sum_purch = []
	tot_cluster = []

	for cluster in allclusters:
		lst_purch.append(np.median(cluster[1]['last_purchase_seconds']))
		tot_purch.append(np.median(cluster[1]['total_purchases']))
		avg_purch.append(np.mean(cluster[1]['average_expense']))
		sum_purch.append(np.sum(cluster[1]['total_purchases']))
		tot_cluster.append(len(cluster[1]['average_expense']))



	medians = []
	medians2 = []
	for cluster_label in range(4):
		cluster_data = used_data[labels == cluster_label]
		cluster_median = np.median(cluster_data, axis=0)
		cluster_median2 = np.median(cluster_data, axis=1)
		medians.append(cluster_median)
		medians2.append(cluster_median2)


	plt.figure(100)
	plt.barh(['New customer', 'Slowly engaging customer', 'Moderately valuable customer at risk', 'Highly valuable customer at high risk'], tot_cluster)


	plt.xlabel("Number of customers")



	plt.figure(200)
	sum_sum_purch = sum(sum_purch)
	plt.scatter(lst_purch, avg_purch, c=['blue', 'green', 'orange', 'magenta'], s=sum_purch / (sum_sum_purch / 900))

	n = ['New customer', 'Moderately valuable customer at risk', 'Slowly engaging customer', 'Highly valuable customer at high risk']

	for i, txt in enumerate(n):
		plt.annotate(txt, (lst_purch[i], avg_purch[i]))

	plt.xticks(ticks=[0, 2592000, 5184000, 7776000, 10368000], labels=[0, 1, 2, 3, 4])
	plt.xlabel("Median recency (months)")
	plt.ylabel("Median frequency")


	plt.figure(300)

	plt.scatter(used_data['last_purchase_seconds'], used_data['total_purchases'], c=y_means, s=10, cmap='viridis')

	centers = kmeans.cluster_centers_
	plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
	plt.xticks(ticks=[0, 2592000, 5184000, 7776000, 10368000], labels=[0, 1, 2, 3, 4])

	plt.xlabel("Last purchase (months)")
	plt.ylabel("Total purchases per customer")

	plt.grid(True)


	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)







if __name__ == '__main__':
    main()

