""" This is the project's framework for the webapp. Made with Flask. """

from flask import Flask, render_template, request, redirect, flash
import datetime
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'theory can only take you so far'


@app.route("/", methods=['POST', 'GET'])
def main_page():

    return render_template('homepage.html')


if __name__ == '__main__':
    Flask.run(app)
