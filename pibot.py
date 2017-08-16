import re
import time
import json
import psutil
from slackclient import SlackClient
import slackcreds

# lifted from http://blog.benjie.me/building-a-slack-bot-to-talk-with-a-raspberry-pi/

hostname = socket.gethostname()
slack_client = SlackClient(slackcreds.slackAuth)


# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == slackcreds.botName:
        slack_user_id = user.get('id')
        break


# Start connection
if slack_client.rtm_connect():
    print "Connected! %s" % slack_user_id

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

                if re.match(r'.*(memory|ram).*', message_text, re.IGNORECASE):
                    mem = psutil.virtual_memory()
                    mem_pct = mem.percent

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="%s: RAM is at %s%%." % (hostname, mem_pct),
                        as_user=True)

        time.sleep(1)
