#!/usr/bin/python3
################################################################################
# luca@glgprograms.it
# GPLv3
################################################################################

from time import sleep
import csv
import sys,os
import gqrxInterface	# must be in the same folder

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

###---------------------------------- MAIN ----------------------------------###
FREQ = []
index = 0
TIME_SLOT = 0.1		# seconds between skips

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

# Open connection with gqrx
try:
	gqrx_conn = gqrxInterface.Gqrx(HOST, PORT)
except ConnectionRefusedError:
	print("Connection refused\nCheck gqrx network settings")
	sys.exit(1)

while(1):
	sql = gqrx_conn.get_squelch()			# read SQUELCH level
	try:
		sql = float(sql)
	except:
		sql = 0		# in case of misreadings, squelch HIGH
		print("Error. sql=", sql)	# DEBUG
	
	sig = gqrx_conn.get_signal()	# read SIGNAL strength
	try:
		sig = float(sig)
	except:
		sig = -100	# in case of misreadings, signal LOW
		print("Error. sig=", sig)	# DEBUG
	
	# if signal strength < squelch level: skip to next FREQ
	if sig <= sql:
		gqrx_conn.set_frequency(int(FREQ[index]))
		index = (index + 1) % len(FREQ)		# circular list
	
	sleep(TIME_SLOT)
