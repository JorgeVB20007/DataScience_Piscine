import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
import datetime
from tqdm import tqdm
import pandas

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

	current_time = init_time
	values = []
	full_values = {}
	dates = []

	print("Making some queries...")
	cur.execute("""CREATE TABLE IF NOT EXISTS purchasers (
	event_time TIMESTAMPTZ,
	user_id BIGINT,
	price FLOAT
	);
	TRUNCATE purchasers;
	INSERT INTO purchasers(event_time, user_id, price)
	SELECT event_time, user_id, price FROM customers WHERE "event_type" = 'purchase';""")

	while (current_time < end_time):
		cur.execute('SELECT COUNT(*) FROM purchasers WHERE "event_time" >= \'{0}\' AND "event_time" < \'{1}\''.format(current_time, current_time + datetime.timedelta(days=1)))
		values.append(cur.fetchone()[0])
		dates.append(current_time)
		cur.execute('SELECT * FROM purchasers WHERE "event_time" >= \'{0}\' AND "event_time" < \'{1}\''.format(current_time, current_time + datetime.timedelta(days=1)))
		full_values[current_time] = cur.fetchall()
		current_time += datetime.timedelta(days=1)


	fig, ax = plt.subplots()

	ax.plot(values)

	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)


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

