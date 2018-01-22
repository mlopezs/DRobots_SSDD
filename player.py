#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
Ice.loadSlice('--all services.ice')
import services

class PlayerI(drobots.Player):

        def __init__(self, mines, containerNumber, name, current=None):

                self.factories = 0
                self.bots = 1
                self.detectors = 0
                self.mine_index = 0
                self.containerNumber = containerNumber
                self.name = name

                if mines == 0:
                        self.mines = [
                                drobots.Point(x=100, y=100),
                                drobots.Point(x=100, y=300),
                                drobots.Point(x=300, y=100),
                                drobots.Point(x=300, y=300)
                        ]
                else:
                        self.mines = [
                                drobots.Point(x=150, y=150),
                                drobots.Point(x=150, y=350),
                                drobots.Point(x=350, y=150),
                                drobots.Point(x=350, y=350)
                        ]

        def makeController(self, bot, current=None):
                
                print("- - - - - CREANDO ROBOT CONTROLLER - - - - -")
                
                broker = current.adapter.getCommunicator()

                print("Creando Container...")

                cproxy = broker.stringToProxy("Container" + self.containerNumber)
                container_prx = services.ContainerPrx.checkedCast(cproxy)

                print("Creando Factory {}...".format(self.factories%3))

                fproxy = broker.stringToProxy("Factory" + str(self.factories%3))
                self.factories += 1
                factory_prx = services.FactoryPrx.checkedCast(fproxy)

                print("Creando robot...")

                robot_prx = factory_prx.make(bot, self.bots, self.containerNumber)

                print("Robot creado con éxito.\nEnlazando con Container {}...".format(self.containerNumber))
        
                container_prx.link("Robot" + str(self.bots), robot_prx)
                self.bots += 1

                print("- - - - - ROBOT CONTROLLER CREADO - - - - -")

                return robot_prx

        def makeDetectorController(self, current):

    	        print("- - - - - CREANDO DETECTOR CONTROLLER - - - - -")

    	        broker = current.adapter.getCommunicator()

    	        print("Creando Container...")

    	        cproxy = broker.stringToProxy("Container" + self.containerNumber)
    	        container_prx = services.ContainerPrx.checkedCast(cproxy)

    	        print("Creando Factory {}...".format(self.factories%3))

    	        fproxy = broker.stringToProxy("Factory" + str(self.factories%3))
    	        self.factories += 1
    	        factory_prx = services.FactoryPrx.checkedCast(fproxy)

    	        print("Creando detector...")

    	        detector_prx = factory_prx.makeDetector(self.containerNumber)

    	        print("Detector creado con éxito.\nEnlazando con Container {}...".format(self.containerNumber))

    	        container_prx.link("Detector" + str(self.detectors), detector_prx)
    	        self.detectors += 1

    	        print("- - - - - DETECTOR CONTROLLER CREADO - - - - -")

    	        return detector_prx

        def getMinePosition(self, current):

    	        print("Poniendo mina {}".format(self.mine_index))
    	        mine_position = self.mines[self.mine_index]
    	        self.mine_index += 1

    	        return mine_position

        def win(self, current=None):

    	        print("You win! Congratulations, {}\n(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧\n".format(self.name))
    	        current.adapter.getCommunicator().shutdown()

        def lose(self, current=None):

    	        print("Oh no! You lose, {}\n(╯°□°）╯︵ ┻━┻\n".format(self.name))
    	        current.adapter.getCommunicator().shutdown()

        def gameAbort(self, current=None):

    	        print("Fuck! Game has crashed\n.·´¯`(>▂<)´¯`·.\n")
    	        current.adapter.getCommunicator().shutdown()
