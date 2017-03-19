#!flask/bin/python
from flask import Flask, render_template
import pymysql
import pandas as pd
app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html',
    						title = 'Home')
    						
@app.route('/chart')
def chart():
	password = 'Eranu2304'
	conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=password, db='bm_scraping', charset='utf8')
	cur = conn.cursor()
	cur.execute('SELECT date, price from paid_articles');
	rows = []
	for row in cur:
		rows.append(row)
	df = pd.DataFrame(rows)
	labels = df[0]
	values = df[1]
	start_date = df[0].iloc[0]
	end_date = df[0].iloc[-1]
	average_price = round(sum(values)/len(values),2)
	conn.close()
	return render_template('chart.html',
							title='Baromontres - courbe de prix',
							values= values,
							labels=labels,
							start_date = start_date,
							end_date = end_date,
							average_price = average_price
							)
	
if __name__ == "__main__":
	app.run()
	