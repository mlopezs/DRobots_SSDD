#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
Ice.loadSlice('--all services.ice')
import services
Ice.loadSlice('--all communication.ice')
import communication
import math
import random

from detector_warning import *
from detecciones_escaneo import *
from objective import *

class AttackerController(communication.AttackerController, communication.State):

	def __init__(self, bot, iden, containerNumber, current):

		self.bot = bot
		self.robotIden = iden
		self.containerNumber = containerNumber
		self.driving = False
		self.destroyed = False
		self.targets = []
		self.resetTargets = 0
		self.friends = []
		self.movementCounter = 0
		self.direction = 0

		print("- - - - - ROBOT {} -> ATTACKER -> FROM CONTAINER {} - - - - -".format(iden, containerNumber))

	def turn(self, current):

		pos = self.bot.location()

		print("Turn of Attacker{} at location {},{}".format(self.iden, pos.x, pos.y))
		
		crashAlert = False

		if self.destroyed == False:

			if pos.x <= 20 or pos.y <= 20 or pos.x >= 380 or pos.y >= 380:

				crashAlert = True

			if !self.driving and self.movementCounter == 0:

				self.bot.drive(self.direction, 100)
				self.driving = True
				print("[Attacker{}] Driving to -> {}".format(self.iden, self.direction))

			if self.movementCounter >= 35 or crashAlert == True:

				self.direction = (self.direction + 180) % 360
				self.bot.drive(self.direction, 100)
				self.movementCounter = 0
				print("[Attacker{}] Re-Driving to -> {}".format(self.iden, self.direction))

			self.movementCounter += 1

			currentState = State(self.robotIden, pos)
			self.sendStatus(currentState, self.containerNumber, current)

			self.selectTarget()

			self.resetTargets += 1

			if self.resetTargets == 10:

				self.targets = []
				self.resetTargets = 0

	def selectTarget(self):

		if self.targets == 0:
			# Hacer algo cuando no haya objetivos
			return

		self.filterTargets()

		hasShooted = False

		for tgt in self.targets:

			if tgt.prioridad == 3:

				self.destroyThis(tgt)				
				hasShooted = True

		if !hasShooted:

			tgt_indx = random.randint(0, len(self.targets) - 1)
			self.destroyTarget(self.targets[tgt_indx])

	def filterTargets():

		for fri in self.friends:
			for nmy in self.targets:

				disX = nmy.posObjetivo.x - fri.x
				disY = nmy.posObjetivo.y - fri.y	

				if math.hypot(disX, disY) < 40:

					self.targets.remove(nmy)

	def destroyTarget(self, target, current=None):

		try:

			print("[Attacker {}] Lanzando misil desde ({}, {}) a ({}, {})".format(self.iden, target.posAtacante.x, 
				target.posAtacante.y, target.posObjetivo.x, target.posObjetivo.y))

			self.bot.cannon(target.direccion, target.distancia)

		except Exception as e:

			print("EXCEPTION: Energía insuficiente para efectuar el lanzamiento")

	def markTarget(self, dirScan, posAtckr, current=None):
		return Objective(dirScan, posAtckr, None, False)

	def robotDestroyed(self, current=None):
		print("; ; ; ; ; ROBOT DESTRUIDO ; ; ; ; ;") ############################### DO SOMETHING

	def sendStatus(self, state, containerNumber, current):

		container_prx = current.adapter.getCommunicator().stringToProxy("Container" + containerNumber)
		container = services.ContainerPrx.checkedCast(container_prx)
		proxy_list = list(container.list().values())

		for prx in proxy_list:

			if prx.ice_isA("::communication::WatcherController"):

				print("[Wtchr] Enviando estado...")

				robot_prx = communication.WatcherControllerPrx.uncheckedCast(prx)
				robot_prx.addState(state)

			elif prx.ice_isA("::communication::AttackerController")

				print("[Atckr] Enviando estado...")

				robot_prx = communication.AttackerControllerPrx.uncheckedCast(prx)
				robot_prx.addState(state)

	def receiveObjectives(self, objective, current=None):

		if objective not in self.targets:
			self.targets.append(objective)

	def receiveAlert(self, warning, current):

		pos = self.bot.location()
		target = Objective(None, pos, warning.location, True)

	def addState(self, state, current=None):
		self.friends.append(state)

class WatcherController(communication.WatcherController, communication.State):

	def __init__(self, bot, iden, containerNumber, current):

		self.bot = bot
		self.robotIden = iden
		self.containerNumber = containerNumber
		self.driving = False
		self.destroyed = False
		self.friends = []
		self.scannedRobots = []
		self.targets = []
		self.movementCounter = 0
		self.direccion = 0

		print("- - - - - ROBOT {} -> WATCHER -> FROM CONTAINER {} - - - - -".format(iden, containerNumber))

	def turn(self, current):

		scannedTargets = []

		pos = self.bot.location()

		self.sendStatus(pos, current)

		print("Turn of {} at location {},{}".format(self.iden, pos.x, pos.y))

		crashAlert = False

		if !self.destroyed:

			if pos.x <= 20 or pos.y <= 20 or pos.x >= 380 or pos.y >= 380:
				crashAlert = True

			if !self.driving:
				
				self.bot.drive(self.direccion, 100)
				self.driving = True
				print("[Watcher{}] Driving to -> {}".format(self.iden, self.direction))

			else:

				if self.movementCounter >= 35 or crashAlert:

					self.direction = (self.direction + 180) % 360
					self.bot.drive(self.direction, 100)
					self.movementCounter = 0
					print("[Watcher{}] Re-Driving to -> {}".format(self.iden, self.direction))

				elif self.movementCounter < 35:

					self.movementCounter += 1
					wide = 20

					for angle in [0, 45, 90, 135, 180, 225, 270, 315]:

						numFoundRobots = self.bot.scan(angle, wide)

						print("[Watcher{}] Realizando escaneo en ({},{}), con angulo {} y amplitud {} ...\nElementos localizados -> {}".format(
							self.robotIden, pos.x, pos.y, angle, wide, numFoundRobots))

						if numFoundRobots > 0:

							detection = DetectionScannerI(angle, wide, nFoundRobots)
							scannedRobots.append(detection)

			self.targets = []

			if len(self.scannedRobots) > 0:
				self.targets = self.checkPositions(pos)

			if len(self.targets) > 0:
				self.sendObjectives(current)

	def checkPositions(self, myPos):

		friendCounter = 0

		for i