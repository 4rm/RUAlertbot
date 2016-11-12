from twilio.rest import TwilioRestClient
from TwilioPasswords import *
import time
import praw
import time
import TwilioReceiveOld
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

messages = client.messages.list()
for message in reversed(messages):
    SMSList=message.body

r=TwilioReceiveOld.login()

while True:
    messages = client.messages.list()
    for message in reversed(messages):
        NewestSMS=message.body
    if SMSList == NewestSMS:
        logNormal('All clear on the RU front')
    if SMSList != NewestSMS:
        logAlert('Something\'s wrong!')
        r.submit(subreddit=subreddit,title=NewestSMS,text=str(NewestSMS)+"\n \n ******** \n \n*^^I ^^am ^^a ^^bot. ^^Do ^^not ^^rely ^^on ^^me ^^for ^^security ^^alerts!* \n \n [^^\[Sign ^^up ^^for ^^text ^^alerts\]](https://personalinfo.rutgers.edu/pi/updateEns.htm) [^^\[RUPD ^^nixle\]](https://local.nixle.com/rutgers-police-department/) [^^[Github]](https://github.com/4rm/RUAlertbot)")
        SMSList=NewestSMS
    time.sleep(10)
