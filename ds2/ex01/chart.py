import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
import datetime
from tqdm import tqdm

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
	end_time = datetime.datetime(2022, 10, 10, 0, 0, 0)

	current_time = init_time
	values = {}

	print("Making some queries...")

	while (current_time < end_time):
		print("A", current_time)
		cur.execute('SELECT COUNT(*) FROM customers WHERE "event_time" >= \'{0}\' AND "event_time" < \'{1}\''.format(current_time, current_time + datetime.timedelta(days=1)))
		print("B", current_time)
		values[init_time] = cur.fetchone()[0]
		print("C", current_time)
		current_time += datetime.timedelta(days=1)
		print("D", current_time)

	# while (current_time < end_time):
	# 	print(current_time)
	# 	current_time += datetime.timedelta(days=1)

	print(values)


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

