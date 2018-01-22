#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
import math
import random
import time

from player import PlayerI


class Client(Ice.Application):

        def run(self, argv):

                broker = self.communicator()

                # Creamos el player con la información del fichero .properties
                properties = broker.getProperties()
                mines = properties.getProperty("PlayerMines")
                containerNumber = properties.getProperty("ContainerNumber")
                name = properties.getProperty("PlayerName") + str(random.randint(1,9))
                servant = PlayerI(mines, containerNumber, name)

                # Paso básico para el uso de objetos distribuidos
        
                adapter = broker.createObjectAdapter("PlayerAdapter")
                id = broker.stringToIdentity(name)
                
                adapter.add(servant, id)	
                
                direct_prx = adapter.createDirectProxy(id)
                
                adapter.activate()
                
                player_prx = drobots.PlayerPrx.checkedCast(direct_prx)
                
                creadorPartida = int(properties.getProperty("CreadorDePartida"))

                print("................. CREADOR DE PARTIDA -> {} ....................".format(creadorPartida))
                
                try:
                        if creadorPartida == 1:
                                
                                game_factory = broker.propertyToProxy("FactoryPartidas")
                                
                                game_factory_prx = drobots.GameFactoryPrx.checkedCast(game_factory)

                                game_factory_prx.makeGame("joseLuisMola", 2)
                                
                                game_prx = broker.stringToProxy("joseLuisMola")
                                
                                print(game_prx)
                                
                                game_prx = drobots.GamePrx.checkedCast(game_prx)
                                
                                print("Connecting to game {} with nickname {}".format(game_prx, name))
                               
                                game_prx.login(player_prx, name)

                                print("Conectado y esperando")
                                                        
                                self.shutdownOnInterrupt()
                                broker.waitForShutdown()

                        elif creadorPartida == 0:
                                
                                game_prx = broker.stringToProxy("joseLuisMola")
                                               
                                game_prx = drobots.GamePrx.checkedCast(game_prx)
                                
                                print("Connecting to game {} with nickname {}".format(game_prx, name))
                                
                                game_prx.login(player_prx, name)
                                
                                self.shutdownOnInterrupt()
                                broker.waitForShutdown()
                                
                except Exception as ex:
                        
                        print("An error has occurred: {}".format(ex))
                        return 1

                return 0
                                
#sys.exit(Client().main(sys.argv))
if __name__ == '__main__':
        client = Client()
        retval = client.main(sys.argv)
        sys.exit(retval)
