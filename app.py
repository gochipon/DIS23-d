
from flask import Flask, render_template, request

app = Flask(__name__)

# getのときの処理
@app.route('/', methods=['GET'])
def get():
	return render_template('index.html')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
	name = request.form['name']
	limit = request.form['limit']
	first_time = request.form['first_time']
	last_time = request.form['last_time']
	max_time = request.form['max_time']
	req = request.form['req']
	print(name,limit, first_time, last_time, max_time, req)
	return render_template('index.html')

if __name__ == '__main__':
	app.run()