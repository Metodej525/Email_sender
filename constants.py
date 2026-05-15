from pathlib import Path

#absolutní cesta do project složky složky
BASE_DIR = Path(__file__).resolve().parent

ROOT_TITLE = ':)'
CONFIG_PATH = 'config.ini'
CONFIG_ENCODING = 'UTF-8'

EMAIL_SECTION = 'EMAIL'
EMAIL_BODY_1 = 'body1'
EMAIL_BODY_2 = 'body2'
EMAIL_BODY_3 = 'body3'
EMAIL_SIGN = 'sign'
EMAIL_SUBJECT = 'subject'
EMAIL_SENDER = 'sender_email'
EMAIL_SMTP_SERVER = 'smtp_server'
EMAIL_SMTP_PORT = 'smtp_port'
EMAIL_USERNAME = 'username'
EMAIL_CC = 'cc'
EMAIL_SIGN_LOGO_PATH = 'sign_logo_path'

SIGNATURE_SECTION = 'SIGNATURE'
SIGNATURE_NAME = 'name'
SIGNATURE_TELEPHONE = 'telephone'
SIGNATURE_POSITION = 'position'
SIGNATURE_DEPARTMENT = 'department'
SIGNATURE_LOGIN = 'login'
SIGNATURE_EMAIL = 'email'

EXCEL_SECTION = 'EXCEL'
EXCEL_PATH = 'path'


