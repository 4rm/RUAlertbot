# RUAlertbot
## Twilio branch
Attempt to implement Twilio

## Goals
- ~~Have RUAlerts sent to Twilio number~~
- ~~Remove dependancy on gmail inbox scanning~~
- ~~Forward alerts from Twilio number to myself so I can receive alerts too~~
- ~~Set up public webserver with static IP~~

## Current Situation
Using FreeDNS (freedns.afraid.org) and AfraidServiceUpdater4 to monitor my public IP. It seems to work, but FreeDNS seems to go down every now and then. Twilio is still on a trial account as well.

## Notes
My testing subreddit is /r/BraveHorizon, so some scrpts might show attempts to post there instead of /r/Rutgers. It's a private subreddit so test posts don't show up in /u/RU_Alert_Bot's history.

RUAlertsTwilio.py sends a request to the Twilio API every few seconds. It works, but is reserouce intensive and slow.
RUAlertsTwilioWEBSERVER.py uses a webserver, but ngrok (free account) doesn't provide a static URL for the Twilio webhook.
