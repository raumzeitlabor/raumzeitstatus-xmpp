#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#	   main.py
#	   
#	   Copyright 2010 Raphael Michel <webmaster@raphaelmichel.de>
#	   
#	   This program is free software; you can redistribute it and/or modify
#	   it under the terms of the GNU General Public License as published by
#	   the Free Software Foundation; either version 2 of the License, or
#	   (at your option) any later version.
#	   
#	   This program is distributed in the hope that it will be useful,
#	   but WITHOUT ANY WARRANTY; without even the implied warranty of
#	   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	   GNU General Public License for more details.
#	   
#	   You should have received a copy of the GNU General Public License
#	   along with this program; if not, write to the Free Software
#	   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#	   MA 02110-1301, USA.
import threading
import time 
import urllib

from jabberbotM import JabberBot, botcmd
import xmpp 

_jid = 'raumzeitstatus@jabber.ccc.de'
_jpw = open('jabberpw').read().strip()

class RZSJabberBot(JabberBot):
	"""Dies ist der RaumZeitStatus-Jabberbot. Wenn ich away bin, ist das RZL zu, wenn ich online bin, offen und wenn ich beschäftigt bin kenne ich den Status nicht.
	
	rami hat mich programmiert. Da ich auf die Schnelle mit python-jabberbot geschrieben bin, habe ich auch so Denglische und zerschossene Ausgaben wie bei 'help'"""

	def __init__( self, jid, password, res = None, debug = False):
		super( RZSJabberBot, self).__init__( jid, password, res, debug)

		self.users = []
		self.message_queue = []
		self.thread_killed = False

	def setstatus(self, show, status=None):
		pres = xmpp.Presence()
		pres.setShow(show)
		if status is not None:
			pres.setStatus(status)
		self.conn.send(pres)
		
	def thread_proc(self):
		while not self.thread_killed:
			status = urllib.urlopen('http://status.raumzeitlabor.de/api/simple').read().strip()
			
			if status == '1':
				self.setstatus('none', 'RaumZeitLabor ist geöffnet')
			elif status == '0':
				self.setstatus('away', 'RaumZeitLabor ist geschlossen')
			else:
				self.setstatus('dnd', 'Status unbekannt')
			for i in range(60):
				time.sleep(1)
				if self.thread_killed:
					return


bc = RZSJabberBot(_jid, _jpw)

th = threading.Thread( target = bc.thread_proc)
bc.serve_forever( connect_callback = lambda: th.start())
bc.thread_killed = True
