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
	items like timestamps, which we need in order to capture biometric data.  I
	have included this in the 
	
_______

Disclaimers:
=============
	The main keylogging part of this application is gathered from "pyxhook.py" an
	API used in a a keylogger available on SourceForge, by Daniel Folkinsteyn.  It
	uses the xlib library to hook the keys and return their values.
