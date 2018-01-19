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

class DetectorControllerI(drobots.DetectorController, comunication.Alerta):
	
	def __init__(self, containerNumber, current=None):
		self.containerNumber = containerNumber

	def alert(self, pos, robots_detected, current):            
		print("Alert: {} robots detected at {},{}".format(robots_detected, pos.x, pos.y))
		self.sendWarning(current)

	def sendWarning(self,current):
		containerNumber = self.containerNumber
		print(":::::::::::::::::::::::::: Enviando aviso ::::::::::::::::::::::::::")
		container_prx = current.adapter.getCommunicator().stringToProxy("Container"+containerNumber)
		container = services.ContainerPrx.checkedCast(container_prx)
		proxy_list = list(container.list().values())
                	
		for i in  range(len(proxy_list)):
			proxyAux = proxy_list[i]
			if(proxyAux.ice_isA("::comunication::OffensiveController")):
				print("Enviando estado a todos mi compañeros")
				robot = comunication.OffensiveControllerPrx.checkedCast(proxy_list[i])
				robot.ola(100,90)

class Alert():
	def __init__(self, current=None):
		pass