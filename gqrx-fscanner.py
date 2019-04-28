#!/usr/bin/python3
################################################################################
# luca@glgprograms.it
# GPLv3
################################################################################

from time import sleep
import telnetlib

HOST = "127.0.0.1"
PORT = 7356

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

tn = telnetlib.Telnet(HOST, PORT)


while(1):
	sql = send_cmd("l SQL")			# read SQUELCH level
	try:
		sql = float(sql)
	except:
		sql = 0		# in case of misreadings, squelch HIGH
		print("Error. sql=", sql)	# DEBUG
	
	sig = send_cmd("l STRENGTH")	# read SIGNAL strength
	try:
		sig = float(sig)
	except:
		sig = -100	# in case of misreadings, signal LOW
		print("Error. sig=", sig)	# DEBUG
	
	# if signal strength < squelch level: skip to next FREQ
	if sig <= sql:
		c = "F " + FREQ[index]
		index = (index + 1) % len(FREQ)		# circular list
		send_cmd(c)
	
	sleep(TIME_SLOT)
