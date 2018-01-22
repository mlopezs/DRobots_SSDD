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

from robot_controller import *
from detector_controller import *

class FactoryI(services.Factory):

	def make(self, robot, nRobots, containerNumber, current):

		print("Creando RobotController...")

		robotController = self.createRobotController(robot, nRobots, containerNumber, current)

		servant = current.adapter.addWithUUID(robotController)
		identity = servant.ice_getIdentity()
		direct_prx = current.adapter.createDirectProxy(identity)
		robotController_prx = drobots.RobotControllerPrx.checkedCast(direct_prx)

		print("RobotController creado con éxito")

		return robotController_prx

	def createRobotController(self, robot, nRobots, containerNumber, current):

		if robot.ice_isA("::drobots::Attacker"):

			print("__________CREANDO ROBOT ATTACKER__________")
			return AttackerController(robot, nRobots, containerNumber, current)

		elif robot.ice_isA("::drobots::Defender"):

			print("__________CREANDO ROBOT DEFENDER__________")
			return DefenderController(robot, nRobots, containerNumber, current)

	def makeDetector(self, containerNumber, current=None):

		print("Creando DetectorController...")

		servant = DetectorControllerI(containerNumber)
		proxy = current.adapter.addWithUUID(servant)
		identity = proxy.ice_getIdentity()
		direct_prx = current.adapter.createDirectProxy(identity)
		detectorController_prx = drobots.DetectorControllerPrx.checkedCast(direct_prx)

		print("DetectorController creado con éxito")

		return detectorController_prx


class ServerFactory(Ice.Application):

	def run(self, argv):

		broker = self.communicator()

		adapter = broker.createObjectAdapter("Factory_Adapter")

		identity_prop = broker.getProperties().getProperty("Identity")
		identity = broker.stringToIdentity(identity_prop)

		servant = FactoryI()

		proxy = adapter.add(servant, identity)

		print("Proxy ServerFactory -> {}".format(proxy))

		adapter.activate()
		
		self.shutdownOnInterrupt()
		broker.waitForShutdown()

		return 0

sys.exit(ServerFactory().main(sys.argv))