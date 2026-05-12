import smtplib
from email.mime.text import MIMEText
import constants as c



# SMTP Configuration
def email_details(config,receiver, body):
    SMTP_SERVER = config.get(c.EMAIL_SECTION,c.EMAIL_SMTP_SERVER)
    SMTP_PORT = int(config.get(c.EMAIL_SECTION,c.EMAIL_SMTP_PORT))
    USERNAME = ''
    PASSWORD = ''

    # Email Details
    sender_email = config.get(c.EMAIL_SECTION,c.EMAIL_SENDER)
    receiver_email = receiver
    subject = config.get(c.EMAIL_SECTION,c.EMAIL_SUBJECT)
    html_body = body
    cc_emails = [
        email.strip()
        for email in config.get(c.EMAIL_SECTION, c.EMAIL_CC).split(',')
    ]
    # Create the email
    message = MIMEText(html_body, "html")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Cc"] = config.get(c.EMAIL_SECTION,c.EMAIL_CC)

    recipients = [receiver_email] + cc_emails

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.sendmail(sender_email, recipients, message.as_string())

    print("HTML email sent successfully!")

