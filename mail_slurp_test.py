from mailslurp_client import ApiClient, Configuration, InboxControllerApi, SendEmailOptions

def test_send_email():
    configuration = Configuration()
    configuration.api_key['x-api-key'] = "00628c20511e7d9bd505668de0a981af6b029a8ba1aa63183bf374fb164a36a5"

    with ApiClient(configuration) as api_client:
        inbox_controller = InboxControllerApi(api_client)
        inbox = inbox_controller.create_inbox(name="TestInbox")
        print("Inbox created successfully with ID:", inbox.id)
        
        try:
            send_options = SendEmailOptions(
                to=["recipient@example.com"],  # Replace with a valid recipient email
                subject="Test Subject",
                body="This is a test email from MailSlurp."
            )
            inbox_controller.send_email(inbox.id, send_email_options=send_options)
            print("Email sent successfully")
        except Exception as e:
            print("Error sending email:", e)

if __name__ == "__main__":
    test_send_email()
