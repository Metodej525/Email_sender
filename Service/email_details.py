import logging
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path

import constants as c



# SMTP Configuration
def email_details(config,receiver, body):



    SMTP_SERVER = config.get(c.EMAIL_SECTION,c.EMAIL_SMTP_SERVER)
    SMTP_PORT = int(config.get(c.EMAIL_SECTION,c.EMAIL_SMTP_PORT))
    USERNAME = ''
    PASSWORD = ''
    raw_body = body + '<img src="cid:logo_image">'
    #signature image manager


    # Email Details
    sender_email = config.get(c.EMAIL_SECTION,c.EMAIL_SENDER)
    receiver_email = receiver
    subject = config.get(c.EMAIL_SECTION,c.EMAIL_SUBJECT)
    html_body = raw_body
    cc_emails = [
        email.strip()
        for email in config.get(c.EMAIL_SECTION, c.EMAIL_CC).split(',')
    ]
    msg = MIMEMultipart('related')

    # Create the email

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Cc"] = config.get(c.EMAIL_SECTION,c.EMAIL_CC)

    msg.attach(MIMEText(html_body, "html"))

    # Attach image
    if getattr(sys, 'frozen', False):
        base_dir = Path(sys.executable).resolve().parent
    else:
        base_dir = c.BASE_DIR

    img_path = base_dir / 'static' / 'img' / 'signature_email_logo.png'

    with open(img_path, "rb") as f:
        img = MIMEImage(f.read())

    img.add_header('Content-ID', '<logo_image>')
    img.add_header('Content-Disposition', 'inline')

    msg.attach(img)

    recipients = [receiver_email] + cc_emails

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.sendmail(sender_email, recipients, msg.as_string())

