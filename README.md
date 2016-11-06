# RUAlertbot
Repo for /u/RU_Alert_bot

## Current functionality
RU Alerts are sent to my phone. SMSForwarder sends these texts to an email address. RUAlerts.py scans my inbox every 20 seconds, looking for unread messages. If one is found, the newest email is posted to /r/Rutgers.

Running off a Raspberry Pi 3 Model B.

## Current issues
- Relying on my phone to forward texts
- Loss of internet prevents reconnect without restart of system
  - Worred about damage over time to my SD card
- Code is redundant in some places and not optimized
  
## Goals
- Implement Twilio
  - Remove dependancy on my phone
  - Possibly remove dependancy on scanning inbox
- Stop restarting Pi after every issue

=========================

##### Disclaimer
Please do not rely on this bot for RUAlerts. Sign up to receive them yourself [here.](https://personalinfo.rutgers.edu/pi/updateEns.htm) I am not an experienced coder and the bot is likely to run into many issues. 

Contact: emilio97@gmail.com
