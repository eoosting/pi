import re
import time
import json
import psutil
import socket
from slackclient import SlackClient
import slackcreds

# from http://blog.benjie.me/building-a-slack-bot-to-talk-with-a-raspberry-pi/

# get the ip address in a string
ipaddr = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

#set the hostname
hostname = socket.gethostname()
# set a regular expression that matches the hostname
hostregexp = r".*(" + re.escape(hostname) + r").*"
#print "hostrexexp set to %s" % hostregexp
# r'.*(cpu).*'
# my_regex = r"\b(?=\w)" + re.escape(TEXTO) + r"\b(?!\w)"

slack_client = SlackClient(slackcreds.slackAuth)


# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == slackcreds.botName:
        slack_user_id = user.get('id')
        break

# Start connection
if slack_client.rtm_connect():
    print "ipannounce.py connected to slack! %s w/ hostname %s" % (slack_user_id, hostname)

    slack_client.api_call(
        "chat.postMessage",
        channel="pibot_announce",
        text="pibot.py startup ... %s reporting in at %s" % (hostname, ipaddr),
        as_user=True
    )

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id):

                print "Message received: %s" % json.dumps(message, indent=2)

                message_text = message['text'].\
                    split("<@%s>" % slack_user_id)[1].\
                    strip()

                if re.match(r'.*(cpu).*', message_text, re.IGNORECASE):
                    cpu_pct = psutil.cpu_percent(interval=1, percpu=False)

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="%s: CPU is at %s%%." % (hostname, cpu_pct),
                        as_user=True)

                if re.match(r'.*(memory|ram|mem).*', message_text, re.IGNORECASE):
                    mem = psutil.virtual_memory()
                    mem_pct = mem.percent

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="%s: RAM is at %s%%." % (hostname, mem_pct),
                        as_user=True)

                if re.match(hostregexp, message_text, re.IGNORECASE):
                    cpu_pct = psutil.cpu_percent(interval=1, percpu=False)
                    mem = psutil.virtual_memory()
                    mem_pct = mem.percent

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="%s: RAM is at %s%% and CPU is at %s%%." % (hostname, mem_pct, cpu_pct),
                        as_user=True)

        time.sleep(1)
