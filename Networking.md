# Creating webhooks for Twilio

To receive text messages from Twilio, we need to expose our localhost to the public. This means creating a "webhook".

![Webhooks](http://i.imgur.com/9Ne9x2r.png)

## ngrok

The primary webhook is currently being supplied by [ngrok](https://ngrok.com/) (pronounced "en-grok"). Special thanks to Alan Shreve (ngrok Founder) for allowing me to use a custom subdomain on a free plan.

![ngrok](http://i.imgur.com/sUtvrmW.png)

Using the command `./ngrok http -subdomain=xxxx 5000` I can launch ngrok on port 5000 at subdomain xxxx.ngrok.io. This is the link I point Twilio to.

To make sure ngrok continues to run (although it seems very stable) I run "ngrokLoop.sh" to make sure it stays up.

    #!/bin/bash
    while true
    do
            ./ngrok http -subdomain=rualert 5000
            sleep 1
    done

## Free DNS

[Free DNS](https://freedns.afraid.org/) is my secondary webhook because of some past issues with speed/stability. While it is not as reliable as ngrok, it is 100% free for everyone and is still an excellent service. Joshua Anderson, founder of Free DNS, was very helpful in answering my questions about setting up a dynamic DNS service.

Free DNS requires that we set up three things: two subdomains, one that points to our full public IP address (no port) and another that points to the previous subdomain with a port, and a dynamic DNS service.

### Subdomains

![FreeDNS Domains](http://imgur.com/OjCXj24.png)

The first domain `subdomain1.domain.com` is a type A DNS record that points to a "hard coded IP address" (explanations of DNS record types [here](https://freedns.afraid.org/faq/type.php)). A type A DNS record will allow us later to update it dynamically. Unfortunately, this domain doesn't point to the open port 5000, which we require.

This is where the second domain comes in. We set up a type CNAME DNS record which points to a URL. In our case we take the first DNS record and append the port we want, so we point to `http://subdomain1.domain.com:5000/`. What this allows us to do it access port 5000 on whatever public IP address we set the initial subdomain to. We can hard code this, but static IP addresses are uncommon and expensive, so we need to set up a dynamic DNS service.

### Dynamic DNS

In order to dynamically update the IP address that our type A DNS record points to, we can add a command to `crontab`. (Windows and Mac systems have programs available [here](https://freedns.afraid.org/scripts/freedns.clients.php)). After installing wget, we append the following command to crontab with `crontab -e`.

    3,8,13,18,23,28,33,38,43,48,53,58 * * * * sleep 52 ; wget --no-check-certificate -O - https://freedns.afraid.org/dynamic/update.php?********************************* >> /tmp/freedns_subdomain1_domain_com.log 2>&1 &

The URL needed can be found at the [Dynamic DNS Update URLs](https://freedns.afraid.org/dynamic/) page on freedns.

In order to check that it's working, run `cat /tmp/freedns_subdomain1_domain_com.log`. If your IP address has not changed, your crontab output should look similar to the following:

![crontab example](http://imgur.com/gV1A0jz.png)

Now, even when your public IP address changes, the crontab script should update the freeDNS IP automatically.
