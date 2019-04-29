#!/usr/bin/python3
################################################################################
# luca@glgprograms.it
# GPLv3
################################################################################

from time import sleep
import telnetlib
import csv
import sys,os

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

if   len(sys.argv) == 1:
	with open("freq.txt", "rt") as f:
		FREQ = f.read().splitlines()
elif len(sys.argv) == 3:
	try:
		lo_freq = int(sys.argv[1])
		hi_freq = int(sys.argv[2])
	except:
		print("Your argument is invalid!")
		sys.exit(-1)
	
	# Open bookmark
	with open(os.path.expanduser("~")+'/.config/gqrx/bookmarks.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		for row in csv_reader:
			if len(row) == 0:
				continue
			if row[0][0] == '#':
				row[0] = row[0][1:]
				labels = [i.strip() for i in row]
			elif labels != None and len(labels) == len(row):
				if len(row) == 6:
					row = [i.strip() for i in row]
					row = dict(zip(labels,row))
					if int(row['Frequency']) < hi_freq and int(row['Frequency']) > lo_freq:
						FREQ.append(row['Frequency'])
					#elif len(labels) == 2:
else:
	print("Usage:")
	print("Read from gqrx bookmarks: ./script low_freq high_freq")
	print("Read from freq.txt      : ./script\n")
	sys.exit(-1)

if len(FREQ) == 0:
    print("No frequencies given")
    sys.exit(1)

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
