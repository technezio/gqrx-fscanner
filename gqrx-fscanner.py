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

def parse_bookmarks(lf, hf):
	'''Parse gqrx bookmark file and extract frequencies between lf and hf'''

	tmp_freq = []

	with open(os.path.expanduser("~")+'/.config/gqrx/bookmarks.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=';')
		for row in csv_reader:
			if len(row) == 0:
				continue
			if row[0][0] == '#':
				row[0] = row[0][1:]
				labels = [i.strip() for i in row]	# Strip out all the spaces
			elif labels != None and len(labels) == len(row) == 5:
				row = [i.strip() for i in row]		# Strip out all the spaces
				row = dict(zip(labels,row))
				if int(row['Frequency']) < hi_freq and int(row['Frequency']) > lo_freq:
					tmp_freq.append(row['Frequency'])
	
	return tmp_freq

def send_cmd(s):
	'''Send a command via telnet and return the answer'''

	cmd = s + '\n'
	cmd = cmd.encode('UTF-8')
	tn.write(cmd)
	sleep(0.1)		# Wait answer
	try:
		a = tn.read_eager()
	except EOFError:
		print("Connection closed")
		sys.exit(1)
	
	return a.decode('UTF-8')

###---------------------------------- MAIN ----------------------------------###
FREQ = []
index = 0
TIME_SLOT = 0.3		# seconds between skips

if len(sys.argv) == 2:
	# Read from txt
	with open(sys.argv[1], "rt") as f:
		FREQ = f.read().splitlines()
elif len(sys.argv) == 3:
	try:
		lo_freq = int(sys.argv[1])
		hi_freq = int(sys.argv[2])
	except:
		print("Your argument is invalid!")
		sys.exit(1)
	
	# Parse gqrx bookmarks
	FREQ = parse_bookmarks(lo_freq, hi_freq)

else:
	print("Usage:")
	print("Read from gqrx bookmarks:   ./script low_freq high_freq")
	print("Read frequencies from file: ./script path/to/file\n")
	sys.exit(1)

if len(FREQ) == 0:
    print("No frequencies given")
    sys.exit(1)

# Open telnet connection with gqrx
try:
	tn = telnetlib.Telnet(HOST, PORT)
except ConnectionRefusedError:
	print("Connection refused\nCheck gqrx network settings")
	sys.exit(1)

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
