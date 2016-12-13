import RUAlertBot
import praw
import os

from flask import Flask, request, redirect, send_from_directory
from twilio.rest import TwilioRestClient
from passwords import *
from twilio import twiml

reddit=praw.Reddit(user_agent=app_ua,client_id=app_id,client_secret=app_secret, username=username, password=password)
client = TwilioRestClient(account_sid, auth_token)
sub='Rutgers'
print('Now posting to ' + sub)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def AlertService():
    TheMessage=request.form.get("Body")
    resp=twiml.Response()
    if TheMessage != None:
        print(TheMessage)
        resp.message(TheMessage,to=ePhone)
        reddit.subreddit(sub).submit(title=TheMessage,selftext=TheMessage+"\n \n ******** \n \n*^^I ^^am ^^a ^^bot." +
        " ^^Do ^^not ^^rely ^^on ^^me ^^for ^^security ^^alerts!* \n \n [^^\[Sign ^^up ^^for ^^text ^^alerts\]]" +
        "(https://personalinfo.rutgers.edu/pi/updateEns.htm) [^^\[RUPD ^^nixle\]](https://local.nixle.com/rutgers-police-department/)" +
        " [^^[Github]](https://github.com/4rm/RUAlertbot)")
    return str(resp)

@app.route("/hello")
def hello():
    return "<h1 style='color: a50000;'>RUAlertBot appears to be operational.</h1><br><a href='https://github.com/4rm/RUAlertbot'>https://github.com/4rm/RUAl$

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
