#!/usr/bin/python
# -*- coding: utf-8 -*-

import 	os
import	re
import 	sys
from		api			import *

DB				= opendb()
FILEH	 		= None
DOWNLIST	= {}
UNAME 		= u""
STIME			= None
ATEXT			= u""
OTEXT			= u""
SID				= None

Q_START = u"INSERT INTO LogSession( UNAME, TIMESTAMP ) VALUES("
Q_DOWN	= u"INSERT INTO KeyLog( SID, TIME, EVENT, SCANCODE, ASCII, TITLE) VALUES("
Q_UP		= u"INSERT INTO KeyLog( SID, TIME, REL, EVENT, SCANCODE, ASCII, TITLE) VALUES("
Q_SUBM	= u"INSERT INTO Submit( SID, ANSWER, SUBMIT ) VALUES("

if len(sys.argv) < 2:
	sys.exit()

def keyDown( OBJ ):
	LID = execute(DB, Q_DOWN + "'" + str(SID) +"', '" + str(OBJ["TIME"]) + "', 0, '" +
			str(OBJ["SCODE"]) + "', '" + str(OBJ["ASCII"]) + "', '" + OBJ["DESC"] + "')", None)[0][0]
	DOWNLIST.update({OBJ["ASCII"]:int(LID)})

def keyUp( OBJ ):
	if OBJ["ASCII"] in DOWNLIST:		#If down event has occured
		EID = DOWNLIST[ OBJ["ASCII"] ]
		execute( DB, Q_UP + "'" + str(SID) + "', '" + str(OBJ["TIME"]) + "', '" + str(EID) + "', 1, '" + str(OBJ["SCODE"]) + "', '" + str(OBJ["ASCII"]) + "', '" + str(OBJ["DESC"]) + "')", None)
		del DOWNLIST[ OBJ["ASCII"] ]

def convert( arg ):
	arg = arg.split(" ")
	obj = {}
	obj.update({"TIME":arg[0]})
	obj.update({"TYPE":int(arg[1])})
	obj.update({"ASCII":arg[2]})
	obj.update({"SCODE":arg[3]})
	obj.update({"DESC":arg[4]})
	return obj

for arg in sys.argv[1:]:
	FILEH = open( arg, "r" )
	
	UNAME = FILEH.readline().decode("utf-8")[:-1]
	STIME	=	FILEH.readline().decode("utf-8")[:-1]
	
	SID = execute( DB, Q_START + "'" + UNAME + "', '" + STIME + "')", None )[0][0]
	SID = int(SID)

	NLINES= FILEH.readline().decode("utf-8")
	NLINES=int(NLINES)
	for i in range(NLINES):
		ATEXT = ATEXT + FILEH.readline().decode("utf-8")
	
	INP = FILEH.readline().decode("utf-8")[:-1]
	while INP != str( NLINES ):
		OBJ = convert( INP )
		if OBJ["TYPE"] == 0:							#Down Event
			keyDown( OBJ )
		if OBJ["TYPE"] == 1:							#Up event
			keyUp( OBJ )
		INP = FILEH.readline().decode("utf-8")[:-1]
		
	OLINES=int(INP)
	for i in range(OLINES):
		OTEXT = OTEXT + FILEH.readline().decode("utf-8")
	FILEH.close()

	ATEXT = re.escape( ATEXT )
	OTEXT = re.escape( OTEXT )
	
	execute(DB, Q_SUBM + "'" + str(SID) + "', '" + ATEXT + "', '" + OTEXT + "')", None)
