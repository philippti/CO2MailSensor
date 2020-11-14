import imaplib
import smtplib
from email.mime.text import MIMEText
import re
from sensor_readout import readout
from sensor_readout import warning


username = "getmyairquality@gmail.com"
password = yourPassword

def fetch_mail():

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(username, password)
    imap.select("Inbox")

    def get_unseen_mail_ids():

        check1, data1 = imap.search(None, "(UNSEEN)")
        mail_ids = re.findall(r'\d', str(data1))

        return mail_ids


    def get_sender_addresses():
        
        ids = get_unseen_mail_ids()
        sender_list = []

        for i in ids:
            check2, data2 = imap.fetch(str(i) , "(BODY[HEADER.FIELDS (FROM)])")
            sender = str(data2)
            addresses = (re.search('<(.*?)>', sender).group(1))
            sender_list.append(addresses)
        
        sender_list = list(set(sender_list))
        
        return sender_list
    return get_sender_addresses()

   
def answer():

    sensor = readout()
    
    smtp_ssl_host = 'smtp.gmail.com'  
    smtp_ssl_port = 465
    sender = 'getmyairquality@gmail.com'

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)

    target = fetch_mail()
    text = "Hello you, \n Thanks for requesting the air quality in Timos room. \n\n CO2: {} ppm  \n TVOC: {} ppb \n Temperature: {:4.2f} °C \n\n Thanks for asking and have a nice day!".format(sensor[0], sensor[1], sensor[2])

    for i in enumerate(target):
        msg = MIMEText(text)
        msg['Subject'] = "Air quality in Timo's room"
        msg['From'] = sender
        msg['To'] = i[1]

        server.sendmail(sender, i[1], msg.as_string())

    server.quit()

answer()

# if(warning()):

#     smtp_ssl_host = 'smtp.gmail.com'  
#     smtp_ssl_port = 465
#     sender = 'yourtrigger@address.com'

#     msg = MIMEText("Please let fresh air in!")
#     msg['Subject'] = "WARNING "*3
#     msg['From'] = sender
#     msg['To'] = "your@mail.com"

#     server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
#     server.login(username, password)
#     server.sendmail(sender, "your@mail.com", msg.as_string() )

