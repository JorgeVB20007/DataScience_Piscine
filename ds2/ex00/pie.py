import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt


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

	print("Executing query 1/4...")
	cur.execute('SELECT COUNT(*) FROM customers WHERE "event_type" = \'remove_from_cart\'')
	rfc = cur.fetchone()[0]
	print("Executing query 2/4...")
	cur.execute('SELECT COUNT(*) FROM customers WHERE "event_type" = \'cart\'')
	cart = cur.fetchone()[0]
	print("Executing query 3/4...")
	cur.execute('SELECT COUNT(*) FROM customers WHERE "event_type" = \'purchase\'')
	purchase = cur.fetchone()[0]
	print("Executing query 4/4...")
	cur.execute('SELECT COUNT(*) FROM customers WHERE "event_type" = \'view\'')
	view = cur.fetchone()[0]


	# view     = 9_654_310
	# cart     = 5_486_521
	# rfc      = 2_748_980
	# purchase = 1_286_088


	labels = ['view', 'cart', 'remove_form_cart', 'purchase']
	values = [view, cart, rfc, purchase]


	fig, ax = plt.subplots()

	ax.pie(values, labels=labels, autopct='%1.1f%%', wedgeprops = {"edgecolor" : "white", 'linewidth': 0.5})
	print(rfc, cart, purchase, view)

	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)

	cur.close()
	conn.close()

if __name__ == '__main__':
    main()

