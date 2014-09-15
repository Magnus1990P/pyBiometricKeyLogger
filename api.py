#!/usr/bin/env python
#-*- coding: utf-8 -*-

import datetime

def getSampleText( fname ):
	filehandle = open( fname, "r" )
	text = filehandle.read().decode("utf-8")
	filehandle.close()

	lines = []
	for i in text.split("\n"):
		if len(i) != 0:
			lines.append( i )
	print lines
	return lines

def getTime( T ):
	s = datetime.datetime.now() - T
	return (s.microseconds + s.seconds * (10**6))

def keyDown( event ):
	t = getTime()
	print t.seconds, t.microseconds

def keyUp( event ):
	t = getTime()
	print t.seconds, t.microseconds
	if event.ScanCode == 9: #IF "ESCAPE" is pressed and released
		hm.cancel()						#Stop the keylogger

