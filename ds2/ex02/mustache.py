import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd

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
	user_id BIGINT,
	price FLOAT
	);
	TRUNCATE purchasers;
	INSERT INTO purchasers(user_id, price)
	SELECT price, user_id FROM customers WHERE "event_type" = 'purchase' ORDER BY price;""")

	print("Getting data from DB...")
	cur.execute("""SELECT * FROM purchasers;""")
	sorted = pd.DataFrame(cur.fetchall())

	print("Loading results...")

	print("count\t{:.6f}".format(sorted.size))
	print("mean\t{:.6f}".format(sorted.mean()[0]))
	print("std\t{:.6f}".format(sorted.median()[0]))
	print("min\t{:.6f}".format(sorted.min()[0]))
	print("25%\t{:.6f}".format(sorted.quantile(0.25)[0]))
	print("50%\t{:.6f}".format(sorted.quantile(0.5)[0]))
	print("75%\t{:.6f}".format(sorted.quantile(0.75)[0]))
	print("max\t{:.6f}".format(sorted.max()[0]))



	plt.figure(100)
	plt.boxplot(sorted[0], notch=True, sym="kd", vert=False, widths=0.9, patch_artist=True)
	
	plt.xlabel("price")
	plt.figure(200)
	plt.boxplot(sorted[0], notch=True, sym="kd", vert=False, widths=0.9, patch_artist=True)
	plt.xlim(-1, 15)
	plt.xlabel("price")


	grouped_users = sorted.groupby(sorted[1])

	averages = grouped_users.mean()

	plt.figure(300)
	plt.boxplot(averages[0], notch=True, sym="kd", vert=False, widths=0.9, patch_artist=True)
	plt.xlabel("price")

	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)







	cur.close()




if __name__ == '__main__':
    main()

