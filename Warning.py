#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
Ice.loadSlice('--all comunication.ice')
import comunication

class Warning(comunication.warning):

	def __init__(self, nRobots, location, current=None):

		self.nRobots = nRobots
		self.location = location
