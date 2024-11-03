""" This is the project's framework for the webapp. Made with Flask. """

from flask import Flask, render_template, request, redirect, flash
import datetime
import pymysql
import mailslurp_client


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



@app.route("/check_threshold", methods=['POST'])
def check_threshold():
    data = request.json
    threshold = data.get('threshold')
    
    # Retrieve the email from the database
    cursor.execute("SELECT email FROM users WHERE condition_met = 1")
    result = cursor.fetchone()
    recipient = result[0] if result else None

    # Define messages based on the threshold value
    if 101 <= threshold <= 150:
        subject = "Breathe Alert"
        message = "If you have preexisting conditions, please stay in bed."
    elif 150 < threshold <= 200:
        subject = "Breathe Alert"
        message = "Please don't go outside."
    else:
        subject = "Breathe Alert"
        message = "DO NOT GO OUTSIDE!"

    # Setting up the MailSlurp client
    configuration = mailslurp_client.Configuration()
    configuration.api_key['x-api-key'] = "00628c20511e7d9bd505668de0a981af6b029a8ba1aa63183bf374fb164a36a5"
    
    with mailslurp_client.ApiClient(configuration) as api_client:
        inbox_controller = mailslurp_client.InboxControllerApi(api_client)
        inbox = inbox_controller.create_inbox(name="BreatheAlert")
        inbox_id = inbox.id
        inbox_email_address = inbox.email_address
        
        # Send the email
        inbox_controller.send_email(inbox_id, recipient, subject, message)

    return {"inbox_id": inbox_id, "inbox_email_address": inbox_email_address}

    
# Main page function
@app.route("/", methods=['POST', 'GET'])
def main_page():

    return render_template('homepage.html')





# Email sending function
@app.route("/send_email", methods=['POST'])
def send_email():
    data = request.json
    recipient = data['recipient']
    subject = data['subject']
    message = data['message']
    
    configuration = mailslurp_client.Configuration()
    configuration.api_key['x-api-key'] = "00628c20511e7d9bd505668de0a981af6b029a8ba1aa63183bf374fb164a36a5"
    
    with mailslurp_client.ApiClient(configuration) as api_client:
        inbox_controller = mailslurp_client.InboxControllerApi(api_client)
        inbox = inbox_controller.create_inbox(name="BreatheAlert")
        inbox_id = inbox.id
        inbox_email_address = inbox.email_address
        
        inbox_controller.send_email(inbox_id, recipient, subject, message)
    
    return {"inbox_id": inbox_id, "inbox_email_address": inbox_email_address}


if __name__ == '__main__':
    Flask.run(app)



