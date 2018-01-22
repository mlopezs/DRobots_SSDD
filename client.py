#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
import math
import random
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

		client_prx = broker.propertyToProxy("Game_proxy")

		game_prx = drobots.GamePrx.checkedCast(client_prx)

		print("Connecting to game {} with nickname {}".format(game_prx, name))

		try:

			game_prx.login(player_prx, name)

			self.shutdownOnInterrupt()
			broker.waitForShutdown()

		except Exception as ex:

			print("An error has occurred: {}".format(ex))
			return 1

		return 0

sys.exit(Client().main(sys.argv))