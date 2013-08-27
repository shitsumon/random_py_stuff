#!/usr/bin/python
"""
ToDo: input check with regexes
"""
from re import match
#import match from re

def checkInput(pattern, value):
	if match(pattern, value):
		return True
	else:
		return False


def getAveragePace(distance, desired_time, isMile):
	
	mile = 1.609344

	if not isMile:
		distance = float(distance)
	else:
		distance = float(distance) * mile

	times = []
	tmp = ""

	for i in range(len(desired_time)):
		if desired_time[i] != ':':
			tmp += desired_time[i]
		else:
			times.append(float(tmp))
			tmp = ""
	
		if i == len(desired_time) - 1:
			times.append(float(tmp))

	minutes = times[1] + times[0] * 60.0
	seconds = times[2] / 100.0

	time = minutes + seconds
	pace = time / distance

	if isMile:
		pace *= mile

	fraction = pace - int(pace)
	seconds = 60.0 * fraction
	
	return str(int(pace)) + ":" + str(int(seconds))


##main
mile = ""
while mile != 'n' and mile != 'y':
	mile = raw_input("Would you like your pace in miles [y/n]: ")

if mile == 'n':
	mile = False
else:
	mile = True

distance = ""

if mile:
	distance = raw_input("What distance will you be running (in miles): ")
else:
	distance = raw_input("What distance will you be running (in kilometres): ")

while not checkInput('^\d*(\.\d*$|$)', distance):
	if mile:
		distance = raw_input("What distance will you be running (in miles): ")
	else:
		distance = raw_input("What distance will you be running (in kilometres): ")


desired_time = raw_input("What time would you like to run (hh:mm:ss): ")

while not checkInput('^\d*:[0-5]\d:[0-5]\d$', desired_time):
	desired_time = raw_input("What time would you like to run (hh:mm:ss): ")

pace = getAveragePace(distance, desired_time, mile)

if mile:
	print "Your average pace should be: %s min/mile" % (pace)
else:
	print "Your average pace should be: %s min/km" % (pace)
