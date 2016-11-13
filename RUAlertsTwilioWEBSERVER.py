from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
import time
from TwilioPasswords import *
import praw
import RUAlertsTwilioWEBSERVER
from passwords import *

def login():
    r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)
    return r

r=RUAlertsTwilioWEBSERVER.login()
client = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def AlertService():
    TheMessage=request.form.get("Body")
    if (TheMessage != None):
        print(TheMessage)
        client.messages.create(to=ePhone, from_=tPhone,body=TheMessage)
        r.submit(subreddit='BraveHorizon',title=TheMessage,text=TheMessage+"\n \n ******** \n \n*^^I ^^am ^^a ^^bot. ^^Do ^^not ^^rely ^^on ^^me ^^for ^^security ^^alerts!* \n \n [^^\[Sign ^^up ^^for ^^text ^^alerts\]](https://personalinfo.rutgers.edu/pi/updateEns.htm) [^^\[RUPD ^^nixle\]](https://local.nixle.com/rutgers-police-department/) [^^[Github]](https://github.com/4rm/RUAlertbot)")
    return str(TheMessage)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")
