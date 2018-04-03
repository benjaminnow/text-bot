import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

class SendEmail:
    def __init__(self):
        self.mailserver = smtplib.SMTP('smtp.gmail.com',587)
        self.mailserver.ehlo()
        self.mailserver.starttls()
        self.mailserver.ehlo()
        self.mailserver.login(config.EMAIL, config.PASSWORD)

    def send_msg(self, person, data, sub):
        msg = MIMEMultipart()
        msg['From'] = config.EMAIL
        msg['To'] = person
        msg['Subject'] = sub
        message = data
        msg.attach(MIMEText(message))
        self.mailserver.sendmail(config.EMAIL,person,msg.as_string())
        print("sent email")
