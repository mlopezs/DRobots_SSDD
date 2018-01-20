#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
Ice.loadSlice('--all services.ice')
import services
Ice.loadSlice('--all comunication.ice')
import comunication

from detector_warning import *

class DetectorControllerI(drobots.DetectorController, comunication.WarningController, ):
	
	def __init__(self, containerNumber, current=None):
		self.containerNumber = containerNumber

	def alert(self, location, detectedRobots, current):            
		print("Alert: {} robots detected at {},{}".format(detectedRobots, location.x, location.y))
		self.sendWarning(detectedRobots, location, current)

	def sendWarning(self, detectedRobots, location, current):
		containerNumber = self.containerNumber
		print(":::::::::::::::::::::::::: Enviando aviso ::::::::::::::::::::::::::")
		container_prx = current.adapter.getCommunicator().stringToProxy("Container"+containerNumber)
		container = services.ContainerPrx.checkedCast(container_prx)
		proxy_list = list(container.list().values())
		detectorWarning = DetectorWarningI(detectedRobots, location)
                	
		for i in  range(len(proxy_list)):
			proxyAux = proxy_list[i]
			if(proxyAux.ice_isA("::comunication::OffensiveController")):
				print("Enviando estado a todos mis compañeros")
				robot = comunication.OffensiveControllerPrx.checkedCast(proxy_list[i])
				robot.receiveAlert(detectorWarning)
