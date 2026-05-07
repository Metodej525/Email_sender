import smtplib
from email.mime.text import MIMEText
import constants as c



# SMTP Configuration
def email_details(receiver, body):
    SMTP_SERVER = c.EMAIL_SMTP_SERVER
    SMTP_PORT = int(c.EMAIL_SMTP_PORT)
    USERNAME = ''
    PASSWORD = ''

    # Email Details
    sender_email = c.EMAIL_SENDER
    receiver_email = receiver
    subject = c.EMAIL_SUBJECT
    html_body = body

    # Create the email
    message = MIMEText(html_body, "html")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("HTML email sent successfully!")