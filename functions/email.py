import smtplib
from email.mime.text import MIMEText
#from tornado.web import asynchronous

WEBSITE_ADDRESS = "http://220.233.10.213:8888"

#@asynchronous
def send_email(recipients, subject="", text=""):
    msg = MIMEText(text)
    msg["Subject"] = subject
    msg["From"] = "donotreply@chs.com"
    msg["To"] = recipients
    s = smtplib.SMTP('localhost')
    s.sendmail(msg["From"], recipients, msg.as_string())
    s.quit()
