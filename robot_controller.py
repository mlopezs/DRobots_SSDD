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
		self.direction = random.randint(0, 359)
		self.pos = 0

		print("- - - - - ROBOT {} -> ATTACKER -> FROM CONTAINER {} - - - - -".format(iden, containerNumber))

	def turn(self, current):

		self.pos = self.bot.location()

		print("Turn of Attacker{} at location {},{}".format(self.robotIden, self.pos.x, self.pos.y))
		
		crashAlert = False

		if self.destroyed == False:

			if self.pos.x <= 20 or self.pos.y <= 20 or self.pos.x >= 380 or self.pos.y >= 380:

				crashAlert = True

			if self.driving == False:

				self.bot.drive(self.direction, 100)
				self.driving = True
				print("[Attacker{}] Driving to -> {}".format(self.robotIden, self.direction))

			else:

				if crashAlert == True:

					self.direction = (self.direction + 180) % 360
					self.bot.drive(self.direction, 100)
					print("[Attacker{}] Re-Driving to -> {}".format(self.robotIden, self.direction))

				else:

					if self.movementCounter >= 35:

						self.direction = random.randint(0, 359)
						self.bot.drive(self.direction, 100)
						self.movementCounter = 0
						print("[Attacker{}] Re-Driving to -> {}".format(self.robotIden, self.direction))

				self.movementCounter += 1

				currentState = drobots.Point(self.pos.x, self.pos.y)
				self.sendStatus(currentState, current)

				self.selectTarget()

				self.resetTargets += 1

				if self.resetTargets == 10:

					self.targets = []
					self.resetTargets = 0

	def selectTarget(self):

		if len(self.targets) == 0:
			# Hacer algo cuando no haya objetivos
			return

		hasShooted = False

		for tgt in self.targets:

			if tgt.prioridad == True:

				self.destroyTarget(tgt)				
				hasShooted = True

		if hasShooted == False:

			if len(self.targets) != 0:
				tgt_indx = random.randrange(0, len(self.targets) - 1 )
				self.destroyTarget(self.targets[tgt_indx])

	def filterTargets(self):

		for fri in self.friends:
			for nmy in self.targets:

				disX = nmy.posObjetivo.x - fri.x
				disY = nmy.posObjetivo.y - fri.y	

				if math.hypot(disX, disY) < 40:

					if nmy in self.targets:
						self.targets.remove(nmy)

	def destroyTarget(self, target, current=None):

		try:

			print("[Attacker {}] Lanzando misil desde ({}, {}) a ({}, {})".format(self.robotIden, target.posAtacante.x, 
				target.posAtacante.y, target.posObjetivo.x, target.posObjetivo.y))

			self.bot.cannon(target.direccion, target.distancia)

		except Exception as e:

			print("EXCEPTION: Energía insuficiente para efectuar el lanzamiento")

	def markTarget(self, dirScan, posAtckr, current=None):
		return Objective(dirScan, posAtckr, None, False)

	def robotDestroyed(self, current=None):

		self.destroyed = True
		print("X X X X X ATTACKER{} DESTRUIDO X X X X X".format(self.robotIden))

	def sendStatus(self, state, current):

		print("[Attacker{}] Sending status...".format(self.robotIden))

		container_prx = current.adapter.getCommunicator().stringToProxy("Container" + self.containerNumber)
		container = services.ContainerPrx.checkedCast(container_prx)
		proxy_list = list(container.list().values())

		for prx in proxy_list:

			if prx.ice_isA("::communication::WatcherController"):

				robot_prx = communication.WatcherControllerPrx.uncheckedCast(prx)
				robot_prx.addState(state)

			elif prx.ice_isA("::communication::AttackerController"):

				robot_prx = communication.AttackerControllerPrx.uncheckedCast(prx)
				robot_prx.addState(state)

	def receiveObjectives(self, objective, current=None):

		if objective not in self.targets:

			if objective.posAtacante is None:

				fullObjective = Objective(None, self.pos, objective.posObjetivo, objective.prioridad)
				self.targets.append(fullObjective)

			else:

				self.targets.append(objective)

	def receiveAlert(self, warning, current):

		pos = self.bot.location()
		target = Objective(None, pos, warning.location, True)
		self.targets.append(target)

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
		self.direction = random.randint(0, 359)

		print("- - - - - ROBOT {} -> WATCHER -> FROM CONTAINER {} - - - - -".format(iden, containerNumber))

	def turn(self, current):

		self.scannedRobots = []

		pos = self.bot.location()

		self.sendStatus(pos, current)

		print("Turn of {} at location {},{}".format(self.robotIden, pos.x, pos.y))

		crashAlert = False

		if self.destroyed == False:

			if pos.x <= 20 or pos.y <= 20 or pos.x >= 380 or pos.y >= 380:
				crashAlert = True

			if self.driving == False:
				
				self.bot.drive(self.direction, 100)
				self.driving = True
				print("[Watcher{}] Driving to -> {}".format(self.robotIden, self.direction))

			else:

				if crashAlert == True:

					self.direction = (self.direction + 180) % 360
					self.bot.drive(self.direction, 100)
					print("[Watcher{}] Re-Driving to -> {}".format(self.robotIden, self.direction))

				elif self.movementCounter >= 35:

					self.direction = random.randint(0, 359)
					self.bot.drive(self.direction, 100)
					self.movementCounter = 0
					print("[Watcher{}] Re-Driving to -> {}".format(self.robotIden, self.direction))

				elif self.movementCounter < 35:

					self.movementCounter += 1
					wide = 20

					for angle in [0, 45, 90, 135, 180, 225, 270, 315]:

						numFoundRobots = self.bot.scan(angle, wide)

						print("[Watcher{}] Realizando escaneo en ({},{}), con angulo {} y amplitud {} ...\nElementos localizados -> {}".format(
							self.robotIden, pos.x, pos.y, angle, wide, numFoundRobots))

						if numFoundRobots > 0:

							detectedObjective = Objective(angle, None, None, False) #DetectionScannerI(angle, wide, numFoundRobots)
							self.scannedRobots.append(detectedObjective)

			self.targets = []

			if len(self.scannedRobots) > 0:
				self.checkPositions(pos)

			if len(self.targets) > 0:
				self.sendObjectives(current)

	def checkPositions(self, myPos):

		friendCounter = 0

		for scn in self.scannedRobots:
			for fri in self.friends:
				
				dx = fri.x - myPos.x
				dy = fri.y - myPos.y

				dis = math.hypot(dx, dy)

				dirScanFri = math.atan2(dy, dx)

				if dirScanFri != scn.direccion:
					self.targets.append(scn)

	def robotDestroyed(self, current=None):

		self.destroyed = True
		print("X X X X X WATCHER{} DESTRUIDO X X X X X".format(self.robotIden))

	def sendStatus(self, state, current):

		print("[Watcher{}] Sending status...".format(self.robotIden))

		container_prx = current.adapter.getCommunicator().stringToProxy("Container" + self.containerNumber)
		container = services.ContainerPrx.checkedCast(container_prx)
		proxy_list = list(container.list().values())

		for prx in proxy_list:

			if prx.ice_isA("::communication::WatcherController"):

				print("[Wtchr] Enviando estado...")

				robot_prx = communication.WatcherControllerPrx.uncheckedCast(prx)
				robot_prx.addState(state)

			elif prx.ice_isA("::communication::AttackerController"):

				print("[Atckr] Enviando estado...")

				robot_prx = communication.AttackerControllerPrx.uncheckedCast(prx)
				robot_prx.addState(state)

	def sendObjectives(self, current):

		print("[Watcher{}] Sending objectives...".format(self.robotIden))

		container_prx = current.adapter.getCommunicator().stringToProxy("Container" + self.containerNumber)
		container = services.ContainerPrx.checkedCast(container_prx)
		proxy_list = list(container.list().values())

		for prx in proxy_list:

			if prx.ice_isA("::communication::AttackerController"):

				robot_prx = communication.AttackerControllerPrx.uncheckedCast(prx)

				for tgt in self.targets:
					robot_prx.receiveObjectives(tgt)

	def addState(self, state, current=None):
		self.friends.append(state)