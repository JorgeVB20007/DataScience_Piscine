import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
import datetime
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

	init_time = datetime.datetime(2022, 10, 1, 0, 0, 0)
	end_time = datetime.datetime(2022, 10, 14, 0, 0, 0)
	# end_time = datetime.datetime(2023, 3, 1, 0, 0, 0)

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
		# tot_income.append(group_df[2].sum())
		# print(">>>", date, "<<<", group_df.count()[0], group_df[2].sum())

	dates_month = []
	grouped = df.groupby(pd.Grouper(key=0, freq='ME'))
	for month, group_df in grouped:
		month = month.replace(day=1)
		dates_month.append(month)
		tot_income.append(group_df[2].sum())
		# print(">>>", month, "<<<", group_df[2])
	dates_month_name = [x.strftime("%b") for x in dates_month]

	# print(df)


	# while (current_time < end_time):
	# 	cur.execute('SELECT COUNT(*) FROM purchasers WHERE "event_time" >= \'{0}\' AND "event_time" < \'{1}\''.format(current_time, current_time + datetime.timedelta(days=1)))
	# 	customer_nbr.append(cur.fetchone()[0])
	# 	dates.append(current_time)
	# 	cur.execute('SELECT * FROM purchasers WHERE "event_time" >= \'{0}\' AND "event_time" < \'{1}\''.format(current_time, current_time + datetime.timedelta(days=1)))
	# 	full_values[current_time] = cur.fetchall()
	# 	current_time += datetime.timedelta(days=1)

	fig = plt.figure()

	ax = fig.add_subplot(111)
	ax1 = fig.add_subplot(211)
	ax2 = fig.add_subplot(212)
#	ax3 = fig.add_subplot(222)


	ax1.plot(dates, tot_users)
	ax2.bar(dates_month, tot_income, width=25)

	ax1.set_xticklabels(dates_month_name)
	ax1.set_xlabel("month")
	ax1.set_ylabel("Number of customers")

	ax2.set_xticks(dates_month_name)
	ax2.set_xticklabels(dates_month_name)
	ax2.set_ylabel("month")
	ax2.set_ylabel("total sales in million of ₳")



	# fig, ax = plt.subplots(2, 2, sharex=True, sharey=False, )

	# plt.figure(1)
	# ax[0, 0].plot(dates, tot_users)

	# print(dates_month)
	# print(tot_income)






	# ax[0, 1].bar(dates_month, tot_income, width=10)
	# plt.gca().set_xticks(dates_month)
	# plt.gca().set_xticklabels(['Oct', 'Nov', 'Dec', 'Jan', 'Feb'])
	# plt.xlabel("month")
	# # ax[0, 1].ylabel("total sales in million of ₳")



	# # ax[0, 0].plot(dates, tot_users, labels=['Oct', 'Nov', 'Dec', 'Jan', 'Feb'])
	# # ax[1, 0].bar(dates, tot_income, labels=['Oct', 'Nov', 'Dec', 'Jan', 'Feb'])






	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)


	# try:
	# 	plt.show()
	# except KeyboardInterrupt as msg:
	# 	print(msg)

	# view     = 9_654_310
	# cart     = 5_486_521
	# rfc      = 2_748_980
	# purchase = 1_286_088


	# labels = ['view', 'cart', 'remove_form_cart', 'purchase']
	# values = [view, cart, rfc, purchase]


	# fig, ax = plt.subplots()

	# ax.pie(values, labels=labels, autopct='%1.1f%%', wedgeprops = {"edgecolor" : "white", 'linewidth': 0.5})
	# print(rfc, cart, purchase, view)

	# try:
	# 	plt.show()
	# except KeyboardInterrupt as msg:
	# 	print(msg)

	cur.close()
	conn.close()

if __name__ == '__main__':
    main()

