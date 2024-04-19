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
	SELECT user_id, price FROM customers WHERE "event_type" = 'purchase' ORDER BY price;""")

	print("Getting data from DB...")
	cur.execute("""SELECT * FROM purchasers;""")
	sorted = pd.DataFrame(cur.fetchall())

	print("Loading results...")

	grouped = sorted.groupby(sorted[0])


	frequencies = grouped.size()
	frequencies = frequencies.value_counts().sort_index()
	grouped_frequencies = frequencies.groupby((frequencies.index - 1) // 8).sum()


	money = grouped.sum()

	money = money.squeeze().sort_values()

	money = money.clip(lower=0, upper=300)

	sorted_money = money.value_counts(bins=6, sort=True)
	money_gaps = [x.left + (x.left - x.right) / 2 for x in sorted_money.index]

	printed_values = []
	a = 0

	for x in sorted_money.values:
		printed_values.append(x * (money_gaps[a] + 25))
		a += 1

	plt.figure(100)

	bars = plt.bar(grouped_frequencies.index * 8 + 4, grouped_frequencies.values, width=8)
	plt.xlim(-1, 41)
	plt.xlabel("frequency")
	plt.ylabel("customers")
	for bar in bars:
		bar.set_edgecolor("white")
		bar.set_linewidth(1)

	plt.figure(200)
	print(money_gaps)

	bars2 = plt.bar([x + 25 for x in money_gaps], printed_values, width=50)
	plt.xlabel("monetary value in ₳")
	plt.ylabel("customers")
	plt.xlim(-40, 250)
	for bar in bars2:
		bar.set_edgecolor("white")
		bar.set_linewidth(1)

	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)







if __name__ == '__main__':
    main()

