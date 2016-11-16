from twilio.rest import TwilioRestClient
import time
import praw
import RUAlertsTwilio
from datetime import datetime
from passwords import *

def logAlert(text):
    print('\t{:%Y-%m-%d %H:%M:%S} - {}'.format(datetime.now(), text))
def logNormal(text):
    print('{:%Y-%m-%d %H:%M:%S} - {}'.format(datetime.now(), text))

def login():
    r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)
    return r

client = TwilioRestClient(account_sid, auth_token)

subreddit='BraveHorizon'

while True:
    try:
        messages = client.messages.list()
        for message in reversed(messages):
            SMSList=message.body
        r=RUAlertsTwilio.login()
        break
    except Exception as e:
        print('Can\'t connect! Retrying in 1 minute...')
        time.sleep(60)

while True:
    try:
        messages = client.messages.list()
        for message in reversed(messages):
            NewestSMS=message.body
        if SMSList == NewestSMS:
            logNormal('All clear on the RU front')
        if SMSList != NewestSMS:
            logAlert('Something\'s wrong!')
            while True:
                try:
                    r.submit(subreddit=subreddit,title=NewestSMS,text=str(NewestSMS)+"\n \n ******** \n \n*^^I ^^am ^^a ^^bot. ^^Do ^^not ^^rely ^^on ^^me ^^for ^^security ^^alerts!* \n \n [^^\[Sign ^^up ^^for ^^text ^^alerts\]](https://personalinfo.rutgers.edu/pi/updateEns.htm) [^^\[RUPD ^^nixle\]](https://local.nixle.com/rutgers-police-department/) [^^[Github]](https://github.com/4rm/RUAlertbot)")
                    print('\t' + NewestSMS)
                    SMSList=NewestSMS
                    break
                except Exception as e:
                    logAlert('Can\'t connect to reddit! Retrying in 1 minute...')
                    time.sleep(60)
        time.sleep(10)
    except Exception as e:
        print('\t' + str(e))
        quit()
              
