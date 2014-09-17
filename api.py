#!/usr/bin/env python
#-*- coding: utf-8 -*-

import datetime
import 	sys
import	MySQLdb


HOST		= "127.0.0.1"
USER		= "root"
PASSWD	= "toor"
DB			= "pyKeyLog"


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


def opendb():
	try:
		CON = MySQLdb.connect( HOST, USER, PASSWD, DB, charset='utf8', use_unicode=True)
		return CON
	except:
		print "ERROR: COULD NOT ESTABLISH CONNECTION TO DATABASE"
		sys.exit()

def execute( CON, QUERY, DATA  ):
	CRSR = CON.cursor()
	try:
		if DATA is not None:
			CRSR.execute( QUERY, (DATA) )
		else:
			CRSR.execute( QUERY )
		
		if "INSERT" in QUERY:
			QUERY = "SELECT LAST_INSERT_ID()"
			CRSR.execute( QUERY )
			
		CON.commit()

		if "SELECT" in QUERY:
			RES = CRSR.fetchall()
			return RES
		return None;
	except MySQLdb.Error, e:
		CON.rollback()
		print e
		print "ERROR: FAILED TO EXECUTE QUERY"
		return None;

