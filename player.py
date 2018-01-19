#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
Ice.loadSlice('--all services.ice')
import drobots
import services

class PlayerI(drobots.Player):
    def __init__(self, minitas,containerNumber ,current=None):
        self.factories = 1
        self.bots = 1
        self.detectors = 0
        self.mine_index = 0
        self.containerNumber = containerNumber

        if minitas == 0:
            self.mines = [
                drobots.Point(x=100, y=100),
                drobots.Point(x=100, y=300),
                drobots.Point(x=300, y=100),
                drobots.Point(x=300, y=300),
            ]
        else:
            self.mines = [
                drobots.Point(x=150, y=150),
                drobots.Point(x=150, y=350),
                drobots.Point(x=350, y=150),
                drobots.Point(x=350, y=350),
            ]
        print(self.mines)

    def makeController(self, bot, current=None):
        containerNumber = self.containerNumber
        broker = current.adapter.getCommunicator()
        print("----- CREANDO ROBOT CONTROLLER -----")

        proxy = current.adapter.getCommunicator().stringToProxy("Container"+containerNumber)
        print("CREANDO CONTAINER EN PROXY: ", proxy)
        container_prx = services.ContainerPrx.checkedCast(proxy)

        print("CREANDO FACTORIAS EN PROXY: "+str(self.factories))
        fproxy = broker.stringToProxy("Factory"+str(self.factories))
        factory_prx = services.FactoryPrx.checkedCast(fproxy)

        robot_prx = factory_prx.make(bot, self.bots, containerNumber)
        print("Robot creado con exito, procediendo a linkear...")
        container_prx.link("Robot" + str(self.bots), robot_prx)
        self.bots += 1

        if (self.factories == 2):
            self.factories = 0

        self.factories += 1

        return robot_prx

    def makeDetectorController(self, current):
        containerNumber = self.containerNumber

        print("----- CREANDO DETECTOR CONTROLLER -----")
        print("CREANDO FACTORIA DE CHIVATOS EN PROXY: "+str(self.factories))
        proxy_factory = current.adapter.getCommunicator().stringToProxy("Factory3")

        proxy = current.adapter.getCommunicator().stringToProxy("Container"+containerNumber)
        print("CREANDO CONTAINER EN PROXY: ", proxy)
        container_prx = services.ContainerPrx.checkedCast(proxy)

        factory = services.FactoryPrx.checkedCast(proxy_factory)
        self.detectors += 1
        detector_proxy = factory.makeDetector(containerNumber)

        container_prx.link("Dectector" + str(self.detectors), detector_proxy)

        return detector_proxy

    def getMinePosition(self, current):

        print("Poniendo minitas...")
        pos = self.mines[self.mine_index]
        self.mine_index += 1

        return pos

    def win(self, current=None):
        print("You win very madafaker well >:D")
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print("You lose madafaker D:<")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print("Game was aborted, like this program")
        current.adapter.getCommunicator().shutdown()
