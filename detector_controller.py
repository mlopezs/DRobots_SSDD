#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
Ice.loadSlice('--all services.ice')
import services
Ice.loadSlice('--all communication.ice')
import communication

from detector_warning import *

class DetectorControllerI(drobots.DetectorController, communication.WarningController):

	def __init__(self, containerNumber, current=None):

		self.containerNumber = containerNumber

	def alert(self, location, detectedRobots, current):

		print("Alert: {} robots detected at ({},{})".format(detectedRobots, location.x, location.y))
		self.sendWarning(detectedRobots, location, current)

	def sendWarning(self, detectedRobots, location, current):

		print(": : : : : : : : : : SENDING WARNING : : : : : : : : : :")

		container_prx = current.adapter.getCommunicator().stringToProxy("Container" + self.containerNumber)
		container = services.ContainerPrx.checkedCast(container_prx)
		proxy_list = list(container.list().values())

		detWarning = DetectorWarningI(detectedRobots, location)

		for prx in proxy_list:
			if prx.ice_isA("::communication::AttackerController"):
				print("Enviado información a robots atacantes...")
				robot = communication.AttackerControllerPrx.checkedCast(prx)
				robot.receiveAlert(detWarning)