import imaplib
import smtplib
from email.mime.text import MIMEText
import re
from sensor_readout import readout                          # import the custom module for reading the sensor data
from sensor_readout import warning


username = yourtrigger@mail.com                             # login credentials for the used email address
password = yourPassword

def fetch_mail():                                           # method for getting incoming mail, extracting sender address and saving them

    imap = imaplib.IMAP4_SSL("imap.gmail.com")              # establishing a SSL secured connection to the imap server of google (if gmail is used)
    imap.login(username, password)
    imap.select("Inbox")                                    # selecting the "Inbox" to answer all incoming mails

    def get_unseen_mail_ids():                               

        check1, data1 = imap.search(None, "(UNSEEN)")       # search for all unseen mails in the inbox
        mail_ids = re.findall(r'\d', str(data1))            # extract the id's as a list of only numbers, hence the use of regex

        return mail_ids


    def get_sender_addresses():                     
        
        ids = get_unseen_mail_ids()                         # get the id's of all unanwered mails
        sender_list = []                                    # empty list for saving the mail addresses of all unanswered mails

        for i in ids:                                       # iteration over all mails to answer
            check2, data2 = imap.fetch(str(i) , "(BODY[HEADER.FIELDS (FROM)])")     # saving the header of the mail in data2, sets the \Seen flag 
            sender = str(data2)                                                     # save raw parsed string from imap.fetch
            addresses = (re.search('<(.*?)>', sender).group(1))                     # extract only mail addresses using regex
            sender_list.append(addresses)                                           # save all addresses in sender_list
        
        sender_list = list(set(sender_list))                                        # eliminate all multiple entries for not answering the same mail more than once
        
        return sender_list
    return get_sender_addresses()

   
def answer():

    sensor = readout()                                      # get the sensor data in a tuple
    
    smtp_ssl_host = 'smtp.gmail.com'                        # sending mail via smtp (if gmail is used)
    smtp_ssl_port = 465
    sender = 'getmyairquality@gmail.com'

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port) # establishing SSL secured smtp connection
    server.login(username, password)

    target = fetch_mail()                                   # get the mail addresses
    text = "Hello you, \n Thanks for requesting the air quality in Timos room. \n\n CO2: {} ppm  \n TVOC: {} ppb \n Temperature: {:4.2f} °C \n\n Thanks for asking and have a nice day!".format(sensor[0], sensor[1], sensor[2])

    for i in enumerate(target):                             # answering all mail addresses in target 
        msg = MIMEText(text)
        msg['Subject'] = "Air quality in Timo's room"
        msg['From'] = sender
        msg['To'] = i[1]

        server.sendmail(sender, i[1], msg.as_string())

    server.quit()

answer()                                                    # answer() serves as a kind of main function

# if(warning()):                                            # optional warning system if CO2 concentration in the rooms reaches a set threshold
                                                            # omitted here, because sensor does not work reliable, avoiding a lot of spam mail
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

