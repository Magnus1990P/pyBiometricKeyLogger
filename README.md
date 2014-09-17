pyBiometricKeylogger
===================

_______

Dependencies:
=============

	* python-pyside.qtcore
	* python-pyside.qtgui
	* python-xlib

_______

Functionality:
=============
	This program uses the "pyxhook.py" API taken from an application on
	SourceForge which is a keylogger for Linux.  This application misses some
	items like timestamps, which we need in order to capture metrics for our 
	biometric data.  I have included this in my keylogger using datetime for ease
	and the high resolution of time in down to microseconds.  Its validity is
	however in question since we are capturing the timestamps as we are printing
	their data to file, which adds some delay.

	To minimize this we are running the keylogging outside of our GUI app. The
	pyxhook.py will give a call to the handler functions globally in the
	application and by that way let it print out data as fast as possible.

	In normal typing setting it shoul not matter, but in a speed typing situation
	it might affect.
	
_______

Disclaimers:
=============
	The main keylogging part of this application is gathered from "pyxhook.py" an
	API used in a a keylogger available on SourceForge, by Daniel Folkinsteyn.  It
	uses the xlib library to hook the keys and return their values.
