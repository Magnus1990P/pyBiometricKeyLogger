#!/usr/bin/env python
# -*- coding: utf-8 -*-
import	datetime
import	sys
from 		PySide.QtCore		import *
from		PySide.QtGui		import *
from 		pyxhook 				import HookManager
from 		api							import *

##VARS
K_D			= 0				#Key Down event
K_U			= 1				#Key Up event
T_START = None		#Start of text
T_END		= None		#End of test
STATE		= False		#State of logging. False = Not logging
WFNAME	= "./scimeth_"
FILEH		= None
HM 			= HookManager()
HM.HookKeyboard()


def writeEvent( e, K, M ):
	global FILEH
	s = getTime( T_START )
	st=str(s)+" "+str(K)+" "+str(e.ScanCode)+" "+str(e.Ascii)+" "+str(e.Key)+"\n"
	FILEH.write(	st.encode("utf-8") )

def keyDown( e ):
	if STATE:
		writeEvent( e, K_D, " Pressing: " + str( e.ScanCode ) )
	
def keyUp( e ):
	if STATE:
		writeEvent( e, K_U, " Released: " + str( e.ScanCode ) )

HM.KeyDown	= keyDown
HM.KeyUp		= keyUp
HM.start()
app			= None

class Application( QWidget ):
	LINES		= getSampleText( "text.txt" )
	OLINES 	= []
	LINE		= 0						#Which line it is on
	FONT		= QFont("Courier New", 11)

	def __init__( self ):
		super( Application, self ).__init__()
		self.START	= QPushButton( "Start Logging" )
		self.START.setFont( self.FONT )
		self.QUIT		= QPushButton( "!!! EXIT APPLICATION !!!" )
		self.QUIT.setFont( self.FONT )

		self.S_TXT	= QTextEdit( )	#Sample text box
		self.S_TXT.setReadOnly( True )	
		self.S_TXT.setFont( self.FONT )
		
		self.W_TXT	= QTextEdit( )	#Data text box
		self.W_TXT.setReadOnly( True )
		self.W_TXT.setFont( self.FONT )

		self.I_TXT	= QLineEdit( )	#Input text box
		self.I_TXT.setFixedHeight( 50 )
		self.I_TXT.setFont( self.FONT )
		self.I_TXT.setReadOnly(True)

		self.U_TXT	= QLineEdit( "JØACKSON".decode("utf-8") )	#Input text box
		self.U_TXT.setFont( self.FONT )

		self.CONT		= QVBoxLayout( )
		self.MBOX		= QVBoxLayout( )
	
		self.MBOX.addWidget( self.U_TXT )
		self.MBOX.addWidget( self.QUIT )
		self.MBOX.addWidget( self.W_TXT )
		self.MBOX.addWidget( self.S_TXT )
		self.MBOX.addWidget( self.I_TXT )
		self.MBOX.addWidget( self.START )

		self.CONT.addLayout( self.MBOX )
		self.S_TXT.setFixedHeight( 30 )

		self.setLayout( self.CONT )

		self.START.clicked.connect(	self.start )
		self.QUIT.clicked.connect(	self.exit )
		self.I_TXT.returnPressed.connect( self.commitLine )
		
	def commitLine( self ):
		self.W_TXT.append(	"<b>SYS: </b><font color='green'>"	+ 
												self.LINES[ self.LINE ][:-1]	+ 
												"</font>\n" )
		self.OLINES.append( self.I_TXT.text())
		self.W_TXT.append(	"<b>YOU: </b><font color='red'>" + 
												self.I_TXT.text() +	"</font>\n" )
		self.I_TXT.clear()
		self.LINE = self.LINE + 1
		self.loadLine()
		
	def loadLine( self ):
		if self.LINE == len( self.LINES ):
			self.stop()
		else:
			self.S_TXT.clear()
			self.S_TXT.append( self.LINES[ self.LINE ] )
			h = self.S_TXT.document().size().height()
			h = h + self.S_TXT.contentsMargins().top()*2 
			self.S_TXT.setFixedHeight( h )

	def	initWrite( self ):
		global FILEH
		FILEH = open( WFNAME, "w" )
		FILEH.write( self.U_TXT.text().encode("utf-8") + "\n" )
		FILEH.write( str( T_START ) + "\n" )
		FILEH.write( str( len( self.LINES ) ) + "\n" )
		for l in self.LINES:
			FILEH.write( l.encode("utf-8") + "\n" )


	def start( self ):
		global T_START, STATE, WFNAME
		if STATE == False and self.U_TXT.text() != "USERNAME":
			T_START = datetime.datetime.now()
			WFNAME = "./session_" + self.U_TXT.text() + str(T_START.strftime("%Y%m%d_%H%M%S") ) + ".log"
			self.initWrite()
			self.LINE	= 0
			STATE = True
			self.loadLine()
			self.I_TXT.setReadOnly(False)
			self.START.setEnabled(False)
			self.I_TXT.setFocus()

	def stop( self ):
		global T_END, STATE, FILEH
		if STATE == True:
			T_END = getTime( T_START )
			STATE = False
			self.S_TXT.clear()
			self.I_TXT.clear()
			self.I_TXT.setReadOnly(True)
			self.START.setEnabled(True)
			FILEH.write( str(len( self.OLINES )) + "\n" )
			for l in self.OLINES:
				FILEH.write( l.encode("utf-8") + "\n" )
			FILEH.close()

	def exit( self ):
		self.stop()
		HM.cancel()
		sys.exit()


class Window( QMainWindow ):
	def __init__( self ):
		super( Window, self ).__init__( )
		self.setWindowTitle( "Science Meth - KeyLogger" )
		self.setMinimumSize( 400, 720 )
		self.apptab = QTabWidget( )
		self.setCentralWidget( self.apptab )
		self.apptab.addTab( Application( ), "Keylogger" )
		self.show()

def main():
	app		= QApplication( sys.argv )
	main	= Window( )
	sys.exit( app.exec_( ) )

if __name__ == '__main__':
	main( )

