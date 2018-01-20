#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('drobots.ice')
import drobots
import math
import random
from player import PlayerI

class Client(Ice.Application):
    def run(self, argv):

        broker = self.communicator()
        name = broker.getProperties().getProperty("PlayerName")
        name = name+str(random.randint(1,10))
        containerNumber = broker.getProperties().getProperty("ContainerNumber")
        minas = broker.getProperties().getProperty("PlayerMines")        
        adapter = broker.createObjectAdapter("PlayerAdapter")
        servant = PlayerI(minas, containerNumber, name)

        id = broker.stringToIdentity(name)
        adapter.add(servant, id)

        direct_prx = adapter.createDirectProxy(id)
        adapter.activate()
        player_prx = drobots.PlayerPrx.checkedCast(direct_prx)

        client_prx = broker.propertyToProxy("Game_proxy")
        game_prx = drobots.GamePrx.checkedCast(client_prx)

        try:
            game_prx.login(player_prx, name)

            self.shutdownOnInterrupt()
            self.communicator().waitForShutdown()

        except Exception as ex:
            print("An error has occurred: {}".format(ex))
            return 1

        return 0

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

sys.exit(Client().main(sys.argv))
