""" This is the project's framework for the webapp. Made with Flask. """

from flask import Flask, render_template, request, redirect, flash
import datetime
import pymysql

# Creating the Flask app for development and deployment
app = Flask(__name__)
# Great movie!
app.config['SECRET_KEY'] = 'theory can only take you so far'

# Creating the first connection to our database
db = pymysql.connect(
    host="byfjbhyqlcuhrwqfxi7f-mysql.services.clever-cloud.com",
    user="ulrhleoemwrfziuv",
    password="fGmH4eiPDxk3paoPxy3i",
    database="byfjbhyqlcuhrwqfxi7f",
    autocommit=True)

# Initiating the database cursor for making changes
cursor = db.cursor()

# Connecting to the MySQL database
db.ping()
if cursor.connection is None:
    db.ping()

# Main page function
@app.route("/", methods=['POST', 'GET'])
def main_page():

    return render_template('homepage.html')


if __name__ == '__main__':
    Flask.run(app)
