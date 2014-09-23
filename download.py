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
	pTime = -1
	yTime = 10**10
	xTime = 0
	bSpaces = 0
	kdEvents = 0

	for e in S: #Key UP
		if(pTime == -1):
			pTime = e["ms"]
		
		if e["type"]==1 and e["ascii"] in STACK:#If down event on stack
			kdEvents += 1
			del STACK[ e["ascii"] ]		#delete it from the stack

			if len(STACK) == 0:										#checks if stack is empty
				aTime = aTime + (e["ms"] - pTime)		#increment active time
				pTime = e["ms"]											#update previous Time

		else:	#KeyDown
			STACK.update({e["ascii"]:e['aid']})	#add ascii val to stack
			if len(STACK) == 1:										#If stack is empty
				iTime = iTime + ( e["ms"] - pTime )	#increment idle time
				pTime = e["ms"]											#update previous Time
			if(e["title"] == "BackSpace"):
				bSpaces += 1

		if yTime > e["ms"]:		#Get start Time
			yTime = e['ms']

		if xTime < e["ms"]:		#Get end Time
			xTime = e['ms']
	
	#return active, idle, start, end, total write time
	return aTime, iTime, yTime, xTime, (xTime - yTime), bSpaces, kdEvents

def correctness(submit, answer):
	tota = 0
	tots = 0
	for s, a in zip(submit.split("\\n"), answer.split("\\n")):
		c = 0 
		w = 0
		words = {}
		for word in a.split(" "):
			words[re.sub("[^a-zA-Z]", "", word)] = 1
			tota += 1
		
		for word in s.split(" "):
			word = re.sub("[^a-zA-Z]", "", word)
			tots += 1
			if(word in words):
				c += 1
			else:
				w += 1
			
	return c, w, tota, tots

basics()
u = ""
if "csv" in sys.argv:
	print "Timestamp, Active, Inactive, Ratio, BackSpace, KeyDownEvents, Start, End, TotalTime, Correct, Wrong, TotalWords, TotalWordsTyped"
for session in SESSIONS:
	session.update({"events":getKeys(session["aid"])})
	a, i, s, e, t, bs, kd = getTimes( session["events"] )
	c, w, tota, tots = correctness(session['submit'], session['text'])
	if(session['uname'] != u):
		print session['uname']
		u = session['uname']
	if "csv" in sys.argv:
		fo = "%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d"
	else:
		fo = "%s a:%d\t i:%d\tr:%d%%\tbs:%d\tkd:%d\ts:%d\te:%d\ttot:%d\tc:%d\tw:%d\ttota:%d\ttots:%d\t"
	
	
	print fo % (session["start"], a/10**3, i/10**3, (((a/10**3)*100)/(t/10**3)), bs, kd, s/10**3, e/10**3, t/10**3, c, w, tota, tots)

