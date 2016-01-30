#!/usr/bin/env python3
import gm_manual

index_list = gm_manual.ManualIndex.load()

# Original IRC Bot code:
# Copyright (C) 2011 : Robert L Szkutak II - http://robertszkutak.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys
import socket
import string

HOST = "irc.boredicons.com"
PORT = 6667

CHANNEL = "#bots"

# Character prefix to access the functions.
ACCESSOR = "#"

NICK = "gm-bot"
IDENT = "gm-bot"
REALNAME = "gm-bot"

readbuffer = ""

s=socket.socket( )
s.connect((HOST, PORT))

s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))

joined = False

while 1:
	readbuffer = readbuffer+s.recv(1024).decode("UTF-8")
	temp = str.split(readbuffer, "\n")
	readbuffer=temp.pop( )

	for line in temp:
		line = str.rstrip(line)
		line = str.split(line)

		if(line[0] == "PING"):
			s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
			if not joined:
				print("Joined channel {}.".format(CHANNEL))
				s.send(bytes("JOIN {}\r\n".format(CHANNEL), "UTF-8"));
				joined = True
		if(line[1] == "PRIVMSG"):
			print(line)
			if line[2] != NICK and len(line) > 3:
				if line[3][1] == ACCESSOR:
					command = line[3][2:]
					if command == "help":
						s.send(bytes("PRIVMSG %s %s \r\n" % (line[2], "Usage: {}gm command_name [index]".format(ACCESSOR)), "UTF-8"))
					elif command == "gm":
						index = 0
						if len(line) >= 6:
							index = int(line[5])
						if len(line) < 4:
							s.send(bytes("PRIVMSG %s %s \r\n" % (line[2], "Invalid argument count"), "UTF-8"))
						else:
							s.send(bytes("PRIVMSG %s %s \r\n" % (line[2], index_list.find(line[4], index)), "UTF-8"))
					elif command == "release":
						s.send(bytes("PRIVMSG %s %s \r\n" % (line[2], "GameMaker: Studio release notes: https://www.yoyogames.com/downloads/gm-studio/release-notes-studio.html"), "UTF-8"))
