#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
Ice.loadSlice('--all services.ice')
Ice.loadSlice('--all comunication.ice')
import drobots
import services
import comunication

from robot_controller import *
from detector_controller import *

class FactoryI(services.Factory):
    def make(self, robot, nRobots, containerNumber, current):


        servant_ctrl = self.create_servant(robot, nRobots, containerNumber, current)
        
        controller_prx = current.adapter.addWithUUID(servant_ctrl)
        prx_id = controller_prx.ice_getIdentity()
        direct_prx = current.adapter.createDirectProxy(prx_id)
        robotCtrl_prx = drobots.RobotControllerPrx.checkedCast(direct_prx)
        
        print("Robotillo creado con exito")
        return robotCtrl_prx

    def create_servant(self, robot, nRobots, containerNumber, current):
        if (robot.ice_isA("::drobots::Attacker")):
            print("___________________CREANDO ROBOT ATTACKER___________________")
            return OffensiveController(robot, nRobots, containerNumber, current)
        elif (robot.ice_isA("::drobots::Defender")):
            print("____________________CREANDO ROBOT DEFENDER__________________")
            return SeeingController(robot, nRobots, containerNumber, current)

    def makeDetector(self, containerNumber,current = None):
        print("Creando detector controller")
        servantDController = DetectorControllerI(containerNumber)
        proxyDController = current.adapter.addWithUUID(servantDController)
        direct_DControllerProxy = current.adapter.createDirectProxy(proxyDController.ice_getIdentity())

        detectorController = drobots.DetectorControllerPrx.checkedCast(direct_DControllerProxy)
        print("Detector controller creado con exito")
        return detectorController

class ServerFactory(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        adapter = broker.createObjectAdapter("Factory_Adapter")

        properties = broker.getProperties().getProperty("Identity")
        identidad = broker.stringToIdentity(properties)

        servant = FactoryI()

        proxy_server = adapter.add(servant, identidad)

        print("ServerFactory", str(proxy_server))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

sys.exit(ServerFactory().main(sys.argv))
