#!/usr/bin/python
# -*- coding: utf-8 -*-

import 	os
import	re
import 	sys
from		api			import *

DB				= opendb()
SESSIONS		= []
FILEH	 		= "DATA.CSV"
KEYPRESS	= {}
SID				= None
STIME			= None
UNAME 		= u""
ATEXT			= u""
OTEXT			= u""

Q_BASIC		= u"SELECT a.UNAME, a.AID, a.TIMESTAMP, b.ANSWER, b.SUBMIT FROM LogSession a LEFT JOIN Submit b ON a.AID=b.SID ORDER BY a.UNAME ASC, a.TIMESTAMP ASC"
Q_KEYS		= u"SELECT a.ASCII, a.AID, a.REL, a.TIME, a.TITLE, a.EVENT FROM KeyLog a WHERE a.SID="
Q_PRESS	= u"SELECT a.SID, c.UNAME, c.TIMESTAMP, a.TIME AS D_TIME, b.TIME AS U_TIME, b.TIME-a.TIME AS PRESSTIME FROM KeyLog a JOIN KeyLog b ON a.AID=b.REL LEFT JOIN LogSession c ON a.SID=c.AID WHERE a.EVENT=0 AND a.SID="

def basics( ):
	global DB
	RES = execute(DB, Q_BASIC, None)
	for r in RES:
		b = {}
		b.update({"aid":int(r[1])})
		b.update({"uname":r[0].decode("utf-8")})
		b.update({"start":r[2]})
		b.update({"text":r[3].decode("utf-8")})
		b.update({"submit":r[4].decode("utf-8")})
		SESSIONS.append( b )

def getKeys( AID ):
	global DB
	RES = execute(DB, Q_KEYS+str(AID), None )
	KEYS = []
	for key in RES:
		k = {}
		k.update({"ascii":int(key[0])})
		k.update({"aid":int(key[1])})
		if key[2] == None:
			k.update({"rel":0})
		else:
			k.update({"rel":int(key[2])})
		k.update({"ms":int(key[3])})
		k.update({"title":key[4]})
		k.update({"type":int(key[5])})
		KEYS.append( k )
	return KEYS

def getTimes( S ):
	STACK = {}
	iTime = 0
	aTime = 0
	pTime = 0
	yTime = 10**10
	xTime = 0

	for e in S: #Key UP
		if e["type"]==1 and e["ascii"] in STACK:#If down event on stack
			del STACK[ e["ascii"] ]		#delete it from the stack

			if len(STACK) == 0:										#checks if stack is empty
				aTime = aTime + (e["ms"] - pTime)		#increment active time
				pTime = e["ms"]											#update previous Time

		else:	#KeyDown
			if len(STACK) == 0:										#If stack is empty
				iTime = iTime + ( e["ms"] - pTime )	#increment idle time
				STACK.update({e["ascii"]:e['aid']})	#add ascii val to stack
				pTime = e["ms"]											#update previous Time

		if yTime > e["ms"]:		#Get start Time
			yTime = e['ms']

		if xTime < e["ms"]:		#Get end Time
			xTime = e['ms']
	
	#return active, idle, start, end, total write time
	return aTime, iTime, yTime, xTime, (xTime - yTime)

basics()
for session in SESSIONS:
	session.update({"events":getKeys(session["aid"])})
	a, i, s, e, t = getTimes( session["events"] )
	print session['uname'], session["start"],
	print a/10**6, i/10**6, s/10**6, e/10**6, t/10**6

