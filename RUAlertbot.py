import RUAlertbot
import praw
import os

from flask import Flask, request, redirect, send_from_directory
from twilio.rest import TwilioRestClient
from passwords import *
from twilio import twiml

def login():
    r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)
    return r

r=RUAlertbot.login()
client = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def AlertService():
    TheMessage=request.form.get("Body")
    resp=twiml.Response()
    if TheMessage != None:
        print(TheMessage)
        resp.message(TheMessage,to=ePhone)
        r.submit(subreddit='BraveHorizon',title=TheMessage,text=TheMessage+"\n \n ******** \n \n*^^I ^^am ^^a ^^bot." +
        " ^^Do ^^not ^^rely ^^on ^^me ^^for ^^security ^^alerts!* \n \n [^^\[Sign ^^up ^^for ^^text ^^alerts\]]" +
        "(https://personalinfo.rutgers.edu/pi/updateEns.htm) [^^\[RUPD ^^nixle\]](https://local.nixle.com/rutgers-police-department/)" +
        " [^^[Github]](https://github.com/4rm/RUAlertbot)")
    return str(resp)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
