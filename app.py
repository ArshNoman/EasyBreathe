from flask import Flask, request, jsonify, render_template, flash
import pymysql
import mailslurp_client
import datetime
import schedule
import time
import threading
import mLearning

# Creating the Flask app for development and deployment
app = Flask(__name__)
app.config['SECRET_KEY'] = 'theory can only take you so far'

# Creating the first connection to our MySQL database
db = pymysql.connect(
    host="byfjbhyqlcuhrwqfxi7f-mysql.services.clever-cloud.com",
    user="ulrhleoemwrfziuv",
    password="fGmH4eiPDxk3paoPxy3i",
    database="byfjbhyqlcuhrwqfxi7f",
    autocommit=True
)

# Initiating the database cursor for executing SQL commands
cursor = db.cursor()


# Sends email using mailslurp
def send_email(recipient, subject, message):
    configuration = mailslurp_client.Configuration()
    configuration.api_key['x-api-key'] = "00628c20511e7d9bd505668de0a981af6b029a8ba1aa63183bf374fb164a36a5"

    with mailslurp_client.ApiClient(configuration) as api_client:
        inbox_controller = mailslurp_client.InboxControllerApi(api_client)
        inbox = inbox_controller.create_inbox(name="BreatheAlert")
        inbox_id = inbox.id
        inbox_controller.send_email(inbox_id, recipient, subject, message)


# API endpoint to add email to database
@app.route("/add_email/<email>", methods=['POST'])
def add_email(email):
    db.ping()
    cursor.execute("INSERT INTO userData (email) VALUES (%s)", (email,))
    db.commit()

    subject = "Subscription Confirmation"
    message = f"Hey, you signed up to receive air quality notifications at {email}."
    send_email(email, subject, message)

    return {"status": "Email added", "recipient_email": email}


#  API endpoint for checking the threshold
@app.route("/check_threshold", methods=['POST'])
def check_threshold():
    data = request.json
    threshold = data.get('threshold')

    cursor.execute("SELECT email FROM userData")
    result = cursor.fetchall()
    emails = [row[0] for row in result]

    if 101 <= threshold <= 150:
        subject = "Breathe Alert"
        message = "If you have preexisting conditions, please stay in bed."
    elif 150 < threshold <= 200:
        subject = "Breathe Alert"
        message = "Please don't go outside."
    else:
        subject = "Breathe Alert"
        message = "DO NOT GO OUTSIDE!"

    for email in emails:
        send_email(email, subject, message)

    return {"status": "Threshold alerts sent"}

# Sends weekly air quality alerts
def send_weekly_threshold_alert():
    cursor.execute("SELECT email FROM userData")
    result = cursor.fetchall()
    emails = [row[0] for row in result]

    subject = "Weekly Air Quality Alert"
    message = "Please be careful about air quality this week."

    for email in emails:
        send_email(email, subject, message)


# Creates the schedule for every monday at 7:00 am
def schedule_weekly_alerts():
    schedule.every().monday.at("07:00").do(send_weekly_threshold_alert)
    while True:
        schedule.run_pending()
        time.sleep(60)


# Starting the scheduling thread for weekly alerts
threading.Thread(target=schedule_weekly_alerts, daemon=True).start()


@app.route("/", methods=['POST', 'GET'])
def main_page():

    if request.method == 'POST':
        email = request.form['email']
        city = request.form['location']

        db.ping()
        cursor.execute("INSERT INTO user VALUES (%s, %s)", (email, city))
        db.commit()

        subject = "Subscription Confirmation"
        message = f"You have signed up to receive air quality notifications at {email}."
        send_email(email, subject, message)

    elif request.method == 'GET':
        city = request.form['city']
        date = request.form['date']

        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        prediction = mLearning.make_prediction(date, city)

        return render_template('homepage.html', prediction_list=prediction)

    return render_template('homepage.html')


# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)
