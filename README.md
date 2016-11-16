# RUAlertbot
## Twilio branch
Attempt to implement Twilio

## Goals
- ~~Have RUAlerts sent to Twilio number~~
- ~~Remove dependancy on gmail inbox scanning~~
- ~~Forward alerts from Twilio number to myself so I can receive alerts too~~
- ~~Set up public webserver with static IP~~
- Upgrade Twilio plan

## Issues
- Twilio gives warning "12200 - Schema validation warning" after each text message

## Current Situation
Using ngrok to publish localhost:5000 online, with FreeDNS as a backup.

## Notes
My testing subreddit is /r/BraveHorizon, so some scrpts might show attempts to post there instead of /r/Rutgers. It's a private subreddit so test posts don't show up in /u/RU_Alert_Bot's history.

RUAlertsTwilio.py sends a request to the Twilio API every few seconds. Reserouce intensive and slow.

RUAlertsTwilioWEBSERVER.py uses webhooks.
