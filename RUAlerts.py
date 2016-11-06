##Import Modules
import praw
import imaplib
import email
import time
import getpass
import RUAlerts
import os
from datetime import datetime
from passwords import *

##Set up Reddit authentication
def login():
    r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)

##Attempt to connect to gmail servers
while True:
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        break
    except Exception as e:
        print('Connection error! ' + str(e) + ' Restarting in 5 minutes!')
        time.sleep(300)
        os.system('sudo reboot')

##Log into gmail
while True:
    try:
        #emailpass = getpass.getpass('Please enter the password for' + str(emailaddress) + ': ')
        ##Removed prompt so script can auto login
        mail.login(emailaddress, emailpass)
        mail.select('inbox')
        break
    except imaplib.IMAP4.error:
        print('Incorrect password')

##Log into reddit
while True:
    try:
        r = RUAlerts.login()

        ##Check inbox for unread messages
        ##Code modified from https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
        while 1:
            result, response = mail.uid('search', None, "(UNSEEN)")
            unread_msg_nums = response[0].split()

            result, data = mail.uid('search', None, "ALL")
            latest_email_uid = data[0].split()[-1]
            result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = data[0][1]

            email_message = email.message_from_bytes(raw_email)
            ##If there's an unread message, post the newest email
            ##Doesn't necessarily post the unread message, just the newest one (should always be the same)
            if len(unread_msg_nums)>0:
                print('\t' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' - Something\'s wrong!')
                ##Grab the plaintext from the message
                for part in email_message.walk():
                    if part.get_content_type()=='text/plain':
                        Alert=part.get_payload()
                        ##Attempt to post to reddit (Error if reddit servers are down)
                        while True:
                            try:
                                r.submit(subreddit='Bravehorizon',title=Alert,text=str(Alert)+"\n \n ******** \n \n*^^I ^^am ^^a ^^bot. ^^Do ^^not ^^rely ^^on ^^me ^^for ^^security ^^alerts!* \n \n [^^\[Sign ^^up ^^for ^^text ^^alerts\]](https://personalinfo.rutgers.edu/pi/updateEns.htm) [^^[nixle]](https://local.nixle.com/rutgers-police-department/) [^^[Contact: ^^edg55@scarletmail.rutgers.edu]](mailto://edg55@scarletmail.rutgers.edu)")
                                print('\t' + str(Alert))
                                break
                            except praw.errors.ExceptionList as e:
                                print('\tReddit error!' + str(e) + '\tRetrying in 5 minutes - ' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                #mail.uid('STORE', latest_email_uid, '-FLAGS', '\SEEN')
                                time.sleep(300)
            ##If there's no alert, post an "all clear" (Mostly for debugging)
            else:
                print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' - All clear on the RU front')
                time.sleep(20)
            break
    ##If we can't log into reddit, restart in 2 minutes (possibly redundant)    
    except Exception as e:
        print('\t' + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' - No connection! Restarting in 2 minutes!')
        print('\t' + str(e))
        time.sleep(120)
        os.system("sudo reboot")
