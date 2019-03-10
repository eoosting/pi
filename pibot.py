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

def parse_command (message_text):
	if not len(message_text):  # len of 0 indicates empty message
		message_cmd = "empty"
	elif re.match(r'.*(help).*', message_text, re.IGNORECASE):
		message_cmd = "help"
	elif re.match(r'.*(cpu).*', message_text, re.IGNORECASE):
		message_cmd = "cpu"	
	elif re.match(r'.*(memory|ram|mem).*', message_text, re.IGNORECASE):
		message_cmd = "mem"
	elif re.match(r'.*(version|ver).*', message_text, re.IGNORECASE):
		message_cmd = "ver"
	elif re.match(r'.*(status).*', message_text, re.IGNORECASE):
		message_cmd = "status"
	elif re.match(r'.*(gitupdate).*', message_text, re.IGNORECASE):
		message_cmd = "getupdate"
	else:
		message_cmd = "unknown"
	print "%s command detected" % message_cmd
	return message_cmd

def run_command (message_cmd):
	if message_cmd == 'help':
		slack_client.api_call(
			"chat.postMessage",
			channel=message['channel'],
			text="%s: usage: [all|<hostname>] [help|cpu|mem|ver|status|gitupdate]" % hostname,
#<hostname>: version, ram amd cpu for the named host\n\
#cpu: have all listeners report on cpu\n\
#mem: have all listeners report on memory\n\
#ver: have all listeners report on pibot version and raspbian version" % (hostname),
			as_user=True)

	if message_cmd == 'cpu':
		cpu_pct = psutil.cpu_percent(interval=1, percpu=False)
		slack_client.api_call(
			"chat.postMessage",
			channel=message['channel'],
			text="%s: CPU is at %s%%." % (hostname, cpu_pct),
			as_user=True)	

	if message_cmd == 'cpu':
		mem = psutil.virtual_memory()
		mem_pct = mem.percent
		slack_client.api_call(
			"chat.postMessage",
			channel=message['channel'],
			text="%s: RAM is at %s%%." % (hostname, mem_pct),
			as_user=True)

	if message_cmd == 'ver':
		slack_client.api_call(
			"chat.postMessage",
			channel=message['channel'],
			text="%s: pibot.py %s running on %s issue %s." % (hostname, pibotVersion, systemVersion, systemIssue),
			as_user=True)

	if message_cmd == 'status':
		cpu_pct = psutil.cpu_percent(interval=1, percpu=False)
		mem = psutil.virtual_memory()
		mem_pct = mem.percent

		slack_client.api_call(
			"chat.postMessage",
			channel=message['channel'],
			text="%s: pibot.py %s RAM %s%% CPU %s%%." % (hostname, pibotVersion, mem_pct, cpu_pct),
			as_user=True)

	if message_cmd == 'gitupdate':
		slack_client.api_call(
			"chat.postMessage",
			channel=message['channel'],
			text="%s: ack." % (hostname),
			as_user=True)
		subprocess.check_output(["/home/pi/bin/getgit.sh"])
		subprocess.check_output(["/home/pi/bin/getgit.sh"])
		slack_client.api_call(
			"chat.postMessage",
			channel=message['channel'],
			text="%s: update done." % (hostname),
			as_user=True)

				
	# if re.match(r'.*(procrestart).*', message_text, re.IGNORECASE):
	# 	slack_client.api_call(
	# 		"chat.postMessage",
	# 		channel=message['channel'],
	# 		text="%s: process restart." % (hostname),
	# 		as_user=True)
	# 	os.system('sudo pkill -f \'python /home/pi/bin/pibot.py\'')

	# if re.match(r'.*(osrestart).*', message_text, re.IGNORECASE):
	# 	slack_client.api_call(
	# 		"chat.postMessage",
	# 		channel=message['channel'],
	# 		text="%s: os resrart." % (hostname),
	# 		as_user=True)
	# 	os.system('sudo shutdown -r now')



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
			message_type = message['type']
			if message_type == "message":
				if message['text'].startswith("<@%s>" % slack_user_id):
					message_directed = 'yes'
					message_text = message['text'].\
						split("<@%s>" % slack_user_id)[1].\
						strip()
					print "Directed Message: %s" % message_text
				else:
					message_directed = 'no'
					message_text = message['text'].\
						strip()
					print "Non-Directed Message: %s" % message_text

				if message['text'].startswith("all"):
					print "Message to all %s" % json.dumps(message, indent=2)
					message_text = message_text.\
						split("all")[1].\
						strip()
					print "Message now %" % message_text
					message_to = 'all'
					message_cmd = parse_command(message_text)
					#run_command(message_cmd)
				elif message['text'].startswith(hostname):
					#print "Message to me: %s" % (hostname)
					print "Message to me: %s" % json.dumps(message, indent=2)
					message_text = message_text.\
						split("%s" % hostname)[1].\
						strip()
					print "Message now %s" % message_text
					message_to = 'me'
					message_cmd = parse_command(message_text)
					#run_command(message_cmd)
				else:
					print "Message to not me: %s" % json.dumps(message, indent=2)
					message_to = "notme"

			else:
				print "Non Text Message received: %s" % json.dumps(message, indent=2)

	time.sleep(1)

else:
	print "error: pibot.py %s can not connect to slack! %s w/ hostname %s" % (pibotVersion, slack_user_id, hostname)
