import os
from dotenv import load_dotenv
import psycopg2
import matplotlib.pyplot as plt
import numpy as np


def test_knight(cur, graph_divisions):
	cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'test_knight'")
	test_titles = [title[0] for title in cur.fetchall()]

	fig, ax = plt.subplots(6, 5, figsize=(16, 16))

	curr_graph = 0
	for title in test_titles:
		cur.execute("SELECT \"{}\" FROM test_knight".format(title))
		values = [value[0] for value in cur.fetchall()]
		spacing = np.linspace(min(values), max(values), graph_divisions)
		digitized = np.digitize(values, spacing, right=False)
		y = [0 for _ in range(graph_divisions)]
		for digit in digitized:
			y[digit - 1] += 1
		ax[int(curr_graph / 5), int(curr_graph % 5)].bar(spacing, y, color="#00990088", width=(spacing[2] - spacing[1]), label="Knight")
		ax[int(curr_graph / 5), int(curr_graph % 5)].legend(loc="upper right")
		ax[int(curr_graph / 5), int(curr_graph % 5)].set_title(title)
		# print(values)
		curr_graph += 1

	plt.subplots_adjust(hspace=0.5)
	fig.canvas.set_window_title('Knight\'s stats')
	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)


def train_knight(cur, graph_divisions):
	cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'train_knight'")
	test_titles = [title[0] for title in cur.fetchall()[:-1]]

	fig, ax = plt.subplots(6, 5, figsize=(16, 16))

	cur.execute("SELECT \"knight\" FROM train_knight")
	knights = list(set([value[0] for value in cur.fetchall()]))
	if knights[0] == "Jedi" and knights[1] == "Sith":
		knights[0] = "Sith"
		knights[1] = "Jedi"
	hardcoded_colors = ["#BB000088", "#0000BB88", "#00BB0088", "#77770088", "#77007788", "#00777788"]
	
	curr_graph = 0
	for title in test_titles:
		for knight in range(len(knights)):
			cur.execute("SELECT \"{0}\" FROM train_knight WHERE \"knight\" = '{1}'".format(title, knights[knight]))
			values = [value[0] for value in cur.fetchall()]
			spacing = np.linspace(min(values), max(values), graph_divisions)
			digitized = np.digitize(values, spacing, right=False)
			y = [0 for _ in range(graph_divisions)]
			for digit in digitized:
				y[digit - 1] += 1
			ax[int(curr_graph / 5), int(curr_graph % 5)].bar(spacing, y, color=hardcoded_colors[knight % len(hardcoded_colors)], width=(spacing[2] - spacing[1]), label=knights[knight])
		ax[int(curr_graph / 5), int(curr_graph % 5)].legend(loc="upper right")
		ax[int(curr_graph / 5), int(curr_graph % 5)].set_title(title)
		# print(values)
		curr_graph += 1

	plt.subplots_adjust(hspace=0.5)
	fig.canvas.set_window_title('Many Knights\' stats')
	try:
		plt.show()
	except KeyboardInterrupt as msg:
		print(msg)



def main():
	graph_divisions = 42
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

	test_knight(cur, graph_divisions)
	train_knight(cur, graph_divisions)

	cur.close()
	conn.close()

if __name__ == '__main__':
    main()

