# Serves as the main script, where the answer method serves as the main function. 
# 
# This script is used to connect to a mail server using SSL 
# The mail is fetched and the sender addresses are extracted to send an answer to
# The fetch_mail method only fetches unseen mails and the returns a list of all sender addresses where multiple entries of the same address
# were removed, to avoid multiple answers to the same address
# 
# The sensor readout is handled in the sensor_readout script. The sensor used here is the CCS811.
# The sensor measures the amount of total volatile organic compounds (TVOC) and calculates an equivalent carbon dioxide concentration.
# This calculation is done by assuming the use of the sensor is indoors and the main producer of CO2 are humans
# 
# author: philippti
# date: 20.11.2020

"""
==============================================================================================================================================================================================
"""

""" imports """

import imaplib                                              # imaplib and smtplip are used to connect to the server and fetching the email contents
import smtplib                                              
from email.mime.text import MIMEText                        # MIMEText is used to compose the eMail
import re                                                   # regular expressions are used to extract the mail addresses
from sensor_readout import readout                          # import the custom module for reading the sensor data



""" login credentials """

username = "yourtrigger@mail.com"                           # login credentials for the used email address. These have to be customized
password = "yourpassword"



""" function definitions """

def main():
    answer()                                                 # answer() serves as the main function


def answer():

    sensor = readout()                                      # get the sensor data in a tuple from the custom sensor_readout.py module
    
    smtp_ssl_host = 'smtp.gmail.com'                        # host smtp server of the used mail provider (gmail is used here)
    smtp_ssl_port = 465                                     # SSL port used by SMTP

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port) # establishing SSL secured smtp connection
    server.login(username, password)

    target = fetch_mail()                                   # get the mail addresses
    text = "Hello you, \n Thanks for requesting the air quality in Timos room. \n\n CO2: {} ppm  \n TVOC: {} ppb \n Temperature: {:4.2f} °C \n\n Thanks for asking and have a nice day!".format(sensor[0], sensor[1], sensor[2])

    for i in enumerate(target):                             # answering all mail addresses in target 
        msg = MIMEText(text)
        msg['Subject'] = "Air quality in Timo's room"
        msg['From'] = username
        msg['To'] = i[1]

        server.sendmail(username, i[1], msg.as_string())

    server.quit()



def fetch_mail():                                           # method for getting incoming mail, extracting sender address and saving them

    imap = imaplib.IMAP4_SSL("imap.gmail.com")              # establishing a SSL secured connection to the imap server of google (if gmail is used)
    imap.login(username, password)
    imap.select("Inbox")                                    # selecting the "Inbox" to answer all incoming mails

    def get_unseen_mail_ids():                               

        check1, data1 = imap.search(None, "UNSEEN")       # search for all unseen mails in the inbox
        mail_ids = re.findall(r'\d', str(data1))            # extract the id's as a list of only numbers, hence the use of regex

        return mail_ids


    def get_sender_addresses():                     
        
        ids = get_unseen_mail_ids()                         # get the id's of all unanwered mails
        sender_list = []                                    # empty list for saving the mail addresses of all unanswered mails

        for i in ids:                                       # iteration over all mails to answer
            check2, data2 = imap.fetch(str(i) , "BODY[HEADER]")     # saving the header of the mail in data2, sets the \Seen flag 
            sender = str(data2)                                                     # save raw parsed string from imap.fetch
            addresses = (re.search('<(.*?)>', sender).group(1))                     # extract only mail addresses using regex
            sender_list.append(addresses)                                           # save all addresses in sender_list
        
        sender_list = list(set(sender_list))                                        # eliminate all multiple entries to send only one answer to each sender
        
        return sender_list
    return get_sender_addresses()



""" main function """

if __name__ == "__main__":
    main()