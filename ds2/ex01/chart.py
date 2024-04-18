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
	event_time TIMESTAMPTZ,
	user_id BIGINT,
	price FLOAT
	);
	TRUNCATE purchasers;
	INSERT INTO purchasers(event_time, user_id, price)
	SELECT event_time, user_id, price FROM customers WHERE "event_type" = 'purchase' ORDER BY event_time;""")

	print("Making some queries...")

	cur.execute("SELECT * FROM purchasers;")
	df = pd.DataFrame(cur.fetchall())

	df[0] = pd.to_datetime(df[0])

	grouped = df.groupby(df[0].dt.date)

	dates = []
	tot_users = []
	tot_income = []
	avg_spending = []
	for date, group_df in grouped:
		dates.append(date)
		tot_users.append(group_df.count()[0])

		grouped_users = group_df.groupby(group_df[1])
		daily_user_spending = []
		for user, group_usr in grouped_users:
			daily_user_spending.append(group_usr[2].sum())
		avg_spending.append(sum(daily_user_spending) / len(daily_user_spending))


	dates_month = []
	grouped = df.groupby(pd.Grouper(key=0, freq='ME'))
	for month, group_df in grouped:
		month = month.replace(day=1)
		dates_month.append(month)
		tot_income.append(group_df[2].sum())
	dates_month_name = [x.strftime("%b") for x in dates_month]

	plt.figure(200)
	plt.plot(dates, tot_users)
	plt.xticks(ticks=dates_month, labels=dates_month_name)

	plt.xlabel("month")
	plt.ylabel("Number of customers")


	plt.figure(300)
	plt.bar(dates_month, tot_income, width=25)
	plt.xticks(ticks=dates_month, labels=dates_month_name)

	plt.ylabel("month")
	plt.ylabel("total sales in million of ₳")

	plt.figure(400)
	plt.stackplot(dates, avg_spending)
	plt.xticks(ticks=dates_month, labels=dates_month_name)

	plt.ylabel("month")
	plt.ylabel("average spend/customers in ₳")



	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)

	cur.close()
	conn.close()

if __name__ == '__main__':
    main()

