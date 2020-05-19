import smtplib
import os
from datetime import datetime, timedelta
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def gen_hash():
    today = datetime.now()
    return str(abs(hash(today)))


def send_email(subject, msg):
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    try:
        server = smtplib.SMTP('smtp.office365.com:587')
        server.ehlo()
        server.starttls()
        server.login(email, password)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(email, email, message)
        server.quit()
        print('Email sent')
    except Exception as e:
        print(e)


# Sample
#subject = "MEMEM"
#message = "This is a meme"
#send_email(subject, message)
