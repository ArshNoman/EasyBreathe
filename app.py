from flask import Flask, request, jsonify
import pymysql
import mailslurp_client
import threading
import time
import schedule
import mLearning
from flask_cors import CORS

# Creating the Flask app for development and deployment
app = Flask(__name__)
app.config['SECRET_KEY'] = 'theory can only take you so far'
CORS(app)

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

# Sends email using MailSlurp
def send_email(recipient, subject, message):
    try:
        configuration = mailslurp_client.Configuration()
        configuration.api_key['x-api-key'] = "00628c20511e7d9bd505668de0a981af6b029a8ba1aa63183bf374fb164a36a5"

        with mailslurp_client.ApiClient(configuration) as api_client:
            inbox_controller = mailslurp_client.InboxControllerApi(api_client)
            inbox_id = "f11b4b62-f697-4e99-9f41-6c19d98212ca" 

            send_options = mailslurp_client.SendEmailOptions(
                to=[recipient],
                subject=subject,
                body=message
            )
            inbox_controller.send_email(inbox_id, send_options=send_options)
    except Exception as e:
        print("Error sending email:", e)

@app.route("/add_email", methods=['POST'])
def add_email():
    data = request.get_json()
    email = data.get('email')
    city = data.get('city')  

    if not email or not city:
        return jsonify({"status": "error", "message": "Email and city are required"}), 400

    try:
        # Store the email and city in the database
        cursor.execute("INSERT INTO users (email, city) VALUES (%s, %s)", (email, city))
        db.commit()

        # Prepare the email subject and message
        subject = "Subscription Confirmation"
        message = f"Hey, you signed up to receive air quality notifications at {email}."
        
        # Send the email using MailSlurp
        send_email(email, subject, message)

        return jsonify({"status": "success", "recipient_email": email})
    except Exception as e:
        print("Error adding email to database:", e)
        return jsonify({"status": "error", "message": "Failed to add email"}), 500

# API endpoint for checking the threshold
@app.route("/check_threshold", methods=['POST'])
def check_threshold():
    data = request.json
    threshold = data.get('threshold')

    try:
        cursor.execute("SELECT email FROM users")
        result = cursor.fetchall()
        emails = [row[0] for row in result]

        subject = "Breathe Alert"
        message = ""

        if 101 <= threshold <= 150:
            message = "If you have preexisting conditions, please stay in bed."
        elif 150 < threshold <= 200:
            message = "Please don't go outside."
        else:
            message = "DO NOT GO OUTSIDE!"

        for email in emails:
            send_email(email, subject, message)

        return jsonify({"status": "success", "message": "Threshold alerts sent"})
    except Exception as e:
        print(f"Error checking threshold: {str(e)}")
        return jsonify({"status": "error", "message": "Failed to send threshold alerts"}), 500

# Sends weekly air quality alerts
def send_weekly_threshold_alert():
    try:
        cursor.execute("SELECT email FROM users")
        result = cursor.fetchall()
        emails = [row[0] for row in result]

        subject = "Weekly Air Quality Alert"
        message = "Please be careful about air quality this week."

        for email in emails:
            send_email(email, subject, message)
    except Exception as e:
        print(f"Error sending weekly alerts: {str(e)}")

# Creates the schedule for every Monday at 7:00 am
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
        city = request.form['city']  # Use 'city' instead of 'location'

        try:
            cursor.execute("INSERT INTO users (email, city) VALUES (%s, %s)", (email, city))
            db.commit()

            subject = "Subscription Confirmation"
            message = f"You have signed up to receive air quality notifications at {email}."
            send_email(email, subject, message)

            return jsonify({"status": "success", "message": "Email added successfully!"})
        except Exception as e:
            print(f"Error adding email: {str(e)}")
            return jsonify({"status": "error", "message": "Failed to add email"}), 500

    elif request.method == 'GET':
        city = request.args.get("city")
        date = request.args.get("date")

        predictions = mLearning.make_prediction(date, city)
        return jsonify({'prediction': predictions})

    return jsonify({"status": "error", "message": "Invalid request"}), 400

# API endpoint to test the database connection
@app.route("/test_db", methods=['GET'])
def test_db():
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            result = cursor.fetchone()
            return jsonify({"database_version": result[0]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Running the Flask application
if __name__ == '__main__':
    app.run(debug=True)
