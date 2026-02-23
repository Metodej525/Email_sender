import configparser
import smtplib
from email.mime.text import MIMEText

config= configparser.ConfigParser()
config.read('config.ini', encoding="cp1250")

# SMTP Configuration
SMTP_SERVER = "posta.ikem.cz"  # Replace with actual SMTP server
SMTP_PORT = 587  # 465 for SSL, 587 for TLS
USERNAME = "your_email@example.com"
PASSWORD = "your_password"

# Email Details
sender_email = "no-replyTESTemailAPP@ikem.cz"
receiver_email = "metodej.alexa@ikem.cz"
subject = "HTML Email from Python"
html_body = """\
<html>
  <body>
    <h2>Hello,</h2>
    <p>This is an <b>HTML</b> email sent using <a href="https://python.org">Python</a>.</p>
  </body>
</html>
"""

# Create the email
message = MIMEText(html_body, "html")  # Change "plain" to "html"
message["Subject"] = subject
message["From"] = sender_email
message["To"] = receiver_email

# Send the email
with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()  # Secure connection
    #server.login(USERNAME, PASSWORD)
    server.sendmail(sender_email, receiver_email, message.as_string())

print("HTML email sent successfully!")