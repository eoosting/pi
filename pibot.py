import re
import time
import json
import psutil
import socket
from slackclient import SlackClient
import slackcreds
import subprocess
#from subprocess import call
#import os

pibotVersion = "v1.3.0-alpha1"

issueFile = open("/etc/rpi-issue","r")
issueLines = []
for line in issueFile:
	issueLines.append(line)
systemIssue = issueLines[0].rstrip()
issueFile.close()

releaseFile = open("/etc/os-release","r")
releaseLines = []
for line in releaseFile:
	releaseLines.append(line)
systemVersion = releaseLines[0].rstrip()
releaseFile.close()

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
	print "pibot.py %s connected to slack! %s w/ hostname %s" % (pibotVersion, slack_user_id, hostname)

	# slack_client.api_call(
	# 	"chat.postMessage",
	# 	channel="pibot_announce",
	# 	text="pibot.py %s startup ... %s reporting in at %s" % (pibotVersion, hostname, ipaddr),
	# 	as_user=True
	# )

	while True:
		for message in slack_client.rtm_read():
			if message['type'].startswith("Hello"):
				print "Hello message received: %s" % json.dumps(message, indent=2)
			elif 'text' in message and message['text'].startswith("<@%s>" % slack_user_id):
				print "Message received: %s" % json.dumps(message, indent=2)
				message_text = message['text'].\
					split("<@%s>" % slack_user_id)[1].\
					strip()
			elif 'text' in message and not message['text'].startswith("<@%s>" % slack_user_id):
				print "Non Directed Message received: %s" % json.dumps(message, indent=2)
				if message['text'].startswith("bot"):
					message_text = message['text'].\
						split("bot")[1].\
						strip()
			elif message['type'].startswith("user_typing"):
				print "Typing message received: %s" % json.dumps(message, indent=2)
			else:
				print "Non Text Message received: %s" % json.dumps(message, indent=2)


	time.sleep(1)
else:
	print "error: pibot.py %s can not connect to slack! %s w/ hostname %s" % (pibotVersion, slack_user_id, hostname)