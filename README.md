<h1> <img style="display: inline;" src="http://i.imgur.com/zyq8PXZ.png" alt="Rutgers Snoo" align="right" height=80px width=80px><br>RUAlertbot</h1> 

RUAlertbot is a reddit bot that automatically posts RU Alerts to the Rutgers subreddit [/r/rutgers](https://www.reddit.com/r/rutgers/). It can be found at [/u/RU_Alert_bot](https://www.reddit.com/u/RU_Alert_bot).

<table>
<tr><td><ul>
<b><p align="center">Contents</p></b>
<li><a href="#Tech">Technology used</a></li>
<li><a href="#Webhook">Creating webhooks for Twilio</a></li><ul>
<li><a href="#ngrok">ngrok</a></li>
<li><a href="#FreeDNS">Free DNS</a></li><ul>
<li><a href="#Sub">Subdomains</a></li>
<li><a href="#Dyn">Dynamic DNS</a></li></ul></ul>
<li><a href="How">How it runs</a>
<li><a href="#SpTh">Special Thanks</a></li>
<li><a href="#Dis">Disclaimer</a></li>
</ul></td></tr>
</table>

##<a name="Tech">Technology used</a>

<table>
  <tr>
  <td><a href="http://flask.pocoo.org/">Flask</a></td>
    <td>micro web framework for Python</td>
  </tr>
  <tr>
  <td><a href="http://freedns.afraid.org/">FreeDNS</a></td>
    <td>free subdomain and dynamic DNS hosting</td>
  </tr>
    <tr>
  <td><a href="https://ngrok.com/">ngrok</a></td>
    <td>tunneling service for localhost</td>
  </tr>
    <tr>
  <td><a href="https://praw.readthedocs.io/en/stable/">PRAW</a></td>
    <td>Python Reddit Api Wrapper</td>
  </tr>
    <tr>
  <td><a href="https://www.twilio.com/">Twilio</a></td>
    <td>cloud communications platform</td>
  </tr>
</table>

## <a name="Webhook">Creating webhooks for Twilio</a>

To receive text messages from Twilio, the localhost server of the host PC needs to be exposed to the public.

![Webhooks](http://i.imgur.com/9Ne9x2r.png)

### <a name="ngrok">ngrok</a>

The primary webhook is currently being supplied by [ngrok](https://ngrok.com/) (pronounced "en-grok"). 

![ngrok](http://i.imgur.com/sUtvrmW.png)

Using the command `./ngrok http -subdomain=xxxx 5000` ngrok can be launched on port 5000 at subdomain xxxx.ngrok.io. This is the link Twilio will listen on.

### <a name="FreeDNS">Free DNS</a>

[Free DNS](https://freedns.afraid.org/) is the secondary webhook in case of ngrok becoming unreachable. It is a bit slower than ngrok because two redirects are needed, but it is reliable enough to safely be used as backup.

In order to utilize the FreeDNS service, it requires that three things be set up: a subdomain that points to our full public IP address (no port), a subdomain that points to the previous subdomain (with port), and a dynamic DNS service.

#### <a name="Sub">Subdomains</a>

![FreeDNS Domains](http://imgur.com/OjCXj24.png)

The first domain `subdomain1.domain.com` is a type A DNS record that points to a "hard coded IP address" (explanations of DNS record types [here](https://freedns.afraid.org/faq/type.php)). A type A DNS record allows dynamic updates, which will be discussed later. Unfortunately, this domain doesn't point to the open port 5000, which is required.

This is where the second domain comes in. A type CNAME DNS record, which points to a URL, must be set up. In our case we take the first DNS record and append the port we want, so we point to `http://subdomain1.domain.com:5000/`. What this allows us to do is access port 5000 on whatever public IP address we set the initial subdomain to. This is necessary because the public IP address of the server is likely to change as it is dynamic and not static.

#### <a name="Dyn">Dynamic DNS</a>

In order to dynamically update the IP address that the type A DNS record points to, a command can be added to `crontab`. (Windows and Mac systems have dynamic DNS programs available [here](https://freedns.afraid.org/scripts/freedns.clients.php)). After installing wget, the following command is appended to crontab with `crontab -e`.

    3,8,13,18,23,28,33,38,43,48,53,58 * * * * sleep 52 ; wget --no-check-certificate -O - https://freedns.afraid.org/dynamic/update.php?********************************* >> /tmp/freedns_subdomain1_domain_com.log 2>&1 &

The URL needed can be found at the [Dynamic DNS Update URLs](https://freedns.afraid.org/dynamic/) page on FreeDNS.

In order to check that it's working, one can run `cat /tmp/freedns_subdomain1_domain_com.log`. If the IP address has not changed, the crontab output should look similar to the following:

![crontab example](http://imgur.com/gV1A0jz.png)

Now, even when the public IP address changes, the crontab script should update the freeDNS IP automatically.

## <a name="How">How It Runs</a>
RUAlertbot currently runs off a Raspberry Pi 3 Model B. In order to make sure that RUAlertbot will continue to run even after a power or internet outage, an executable shell script, `myscript.sh`, is set to run at every boot that will launch the necessary programs. This was achieved by adding the following to `rc.local`:

    cd /home/pi/Desktop
    ./myscript.sh
    exit 0

In `myscript.sh`, the following is written to launch the necessary scripts into separate "[tmux](https://tmux.github.io/) sessions"

    #!/bin/bash
    cd /home/pi/RUAlerts
    sudo -u pi tmux new-session -d -s RUAlerts './RUAlertLoop.sh'
    cd /home/pi/ngrok
    sudo -u pi tmux new-session -d -s ngrok './ngrokLoop.sh'

Thus, upon every reboot, `RUAlertLoop.sh` and `ngrokLoop.sh` will run in their own separate session under the `pi` username. Within each shell script is a loop that makes sure the program will continue to run in case of error, e.g.

    #!/bin/bash
    while  true
    do
            python3.5 RUAlerts.py
            sleep 1
    done

With the tmux session launcher `myscript.sh` and the various loop scripts, RUAlertbot should continue to run after a power failure or fatal program error.

## <a name="SpTh">Special Thanks</a>
* Alan Shreve, [ngrok](https://ngrok.com/) Founder, for granting custom domain permissions for free
* Joshua Anderson, [FreeDNS](http://freedns.afraid.org/) Founder, for being extremely helpful and for keeping FreeDNS free

## <a name="Dis">Disclaimer</a>
Please do not rely on this bot for RUAlerts. Sign up to receive them yourself [here.](https://personalinfo.rutgers.edu/pi/updateEns.htm) I am not an experienced coder and the bot is likely to run into issues. 

Contact: emilio97@gmail.com
