#!/usr/bin/python3
################################################################################
# luca@glgprograms.it
# GPLv3
################################################################################

from time import sleep
import telnetlib

# Send a command via telnet and return the answer
def send_cmd(s):
	cmd = s + '\n'
	cmd = cmd.encode('UTF-8')
	tn.write(cmd)
	sleep(0.1)
	try:
		a = tn.read_eager()
	except EOFError:
		print("Connection closed")
		exit(1)
	
	return a.decode('UTF-8')

###---------------------------------- MAIN ----------------------------------###
FREQ = []
index = 0
TIME_SLOT = 0.3		# seconds between skips

with open("freq.txt", "rt") as f:
	FREQ = f.read().splitlines()

tn = telnetlib.Telnet("127.0.0.1", 7356)


while(1):
	sql = send_cmd("l SQL")
	try:
		sql = float(sql)
	except:
		sql = 0
		print("Error. sql=", sql)
	
	sig = send_cmd("l STRENGTH")
	try:
		sig = float(sig)
	except:
		sig = -100
		print("Error. sig=", sig)
	
	# if signal strength < squelch level: skip to next FREQ
	if sig <= sql:
		c = "F " + FREQ[index]
		index = (index + 1) % len(FREQ)
		send_cmd(c)
	
	sleep(TIME_SLOT)
