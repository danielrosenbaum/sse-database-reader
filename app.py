from flask import Flask, render_template, request, make_response
from flaskext.mysql import MySQL
import os
import private

app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = private.user
app.config['MYSQL_DATABASE_PASSWORD'] = private.password
app.config['MYSQL_DATABASE_DB'] = private.db
app.config['MYSQL_DATABASE_HOST'] = private.host

mysql.init_app(app)


@app.route("/")
def main():
	return render_template('homepage.html')

@app.route('/taskOne')
def showTaskOne():
	return render_template('taskone.html')
   
@app.route('/taskTwo')
def showTaskTwo():
	return render_template('tasktwo.html')
    
@app.route('/taskThree')
def showTaskThree():
	return render_template('taskthree.html')

@app.route('/taskFour')
def showTaskFour():
	return render_template('taskfour.html')

@app.route('/queryHandler', methods=['POST'])
def queryHandler():

	# get the input from the html datepicker
	task_db = request.form['task']
	from_date = request.form['from_date']
	to_date = request.form['to_date']

	if from_date and to_date:

		# reformat the input for the dates
		from_year = from_date[6] + from_date[7] + from_date[8] + from_date[9]
		from_month = from_date[0] + from_date[1]
		from_day = from_date[3] + from_date[4]

		to_year = to_date[6] + to_date[7] + to_date[8] + to_date[9]
		to_month = to_date[0] + to_date[1]
		to_day = to_date[3] + to_date[4]

		from_date_val = int(from_year + from_month + from_day)
		to_date_val = int(to_year + to_month + to_day)

		# get the columns 
		columns = "date"
		for col in request.form:
			if col != "from_date" and col != "to_date" and col != "submit_button" and col != "task":
				columns += ", " + col

		# open the connection with MySQL
		conn = mysql.connect()
		cursor = conn.cursor()

		# write and execute the query
		query = "SELECT " + columns + " FROM " + task_db + " WHERE date BETWEEN %s AND %s"
		cursor.execute(query, (from_date_val, to_date_val))

		# get the results from the database
		data = cursor.fetchall()

		# get the file path and name 
		file_path = str(os.path.expanduser('~')) + "/Downloads/"
		file_title = task_db + "_" + str(from_date_val) + "-" + str(to_date_val) 
		file_name = file_title + ".csv"

		# make sure the name is unique so as not to overwrite files
		i = 1
		while os.path.isfile(file_path + file_name):
			file_name = file_title + "_v" + str(i) + ".csv"
			i += 1

		# create file information 
		download_file = columns + "\n"

		for line in data:
			download_file += (str(line).replace("(", "").replace(")", "") + "\n")

		# make data editable in the javascript
		arr = list(data)

		# return a page with the file name and data 
		return render_template('filecreated.html', file_name=file_name, columns=columns, data=arr, download=download_file)

	# an ERROR has occured and the date was not entered fully
	return render_template('errordate.html')

@app.route("/download", methods=['POST'])
def download_csv():  

	# get the file name and file information
	file_name = request.form['download_name']
	csv = request.form['download_file']
			
	# create a response available for download
	response = make_response(csv)
	cd = 'attachment; filename=' + file_name
	response.headers['Content-Disposition'] = cd 
	response.mimetype='text/csv'
	
	return response

if __name__ == "__main__":
	app.run()
