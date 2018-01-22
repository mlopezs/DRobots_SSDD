#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all communication.ice')
import communication

class DetectorWarningI(communication.DetectorWarning):

	def __init__(self, nRobots, location, current=None):

		self.nRobots = nRobots
		self.location = location
