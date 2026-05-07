import smtplib
from email.mime.text import MIMEText
import constants as c



# SMTP Configuration
SMTP_SERVER = c.EMAIL_SMTP_SERVER  # Replace with actual SMTP server
SMTP_PORT = int(c.EMAIL_SMTP_PORT)  # 465 for SSL, 587 for TLS
USERNAME = ''
PASSWORD = ''

# Email Details
sender_email = c.EMAIL_SENDER
receiver_email = ""
subject = c.EMAIL_SUBJECT
html_body = ""

# Create the email
message = MIMEText(html_body, "html")  # Change "plain" to "html"
message["Subject"] = subject
message["From"] = sender_email
message["To"] = receiver_email

# Send the email
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.sendmail(sender_email, receiver_email, message.as_string())

print("HTML email sent successfully!")