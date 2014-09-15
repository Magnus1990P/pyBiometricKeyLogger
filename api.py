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
	return lines

def getTime( T ):
	s = datetime.datetime.now() - T
	return (s.microseconds + s.seconds * (10**6))

