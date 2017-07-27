import re
import time
import json
#import psutil
import socket
from slackclient import SlackClient

slack_client = SlackClient("XXXXXXXXXXX")

ipaddr = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]


# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "pibot1":
        slack_user_id = user.get('id')
        break


# Start connection
if slack_client.rtm_connect():
    print "ipannounce.py connected to slack! %s" % slack_user_id

    slack_client.api_call(
        "chat.postMessage",
        channel="pibot_announce",
        text="reporting in at %s" % ipaddr,
        as_user=True
    )
