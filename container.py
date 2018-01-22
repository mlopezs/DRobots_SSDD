#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all services.ice')
import services

class ContainerI(services.Container):
    def __init__(self):
        self.proxies = dict()

    def link(self, key, proxy, current=None):
        if key in self.proxies:
            print("key in self.proxies")
            raise services.AlreadyExists(key)

        print("link: {0} -> {1}".format(key, proxy))
        self.proxies[key] = proxy

    def unlink(self, key, current=None):
        if not key in self.proxies:
            raise services.NoSuchKey(key)

        print("unlink: {0}".format(key))
        del self.proxies[key]

    def list(self, current=None):
        return self.proxies

class ServerContainer(Ice.Application):
    def run(self, argv):
        print("---------------------- CREANDO CONTAINER ----------------------")
        broker = self.communicator()
        adapter = broker.createObjectAdapter("Container_Adapter")
        servant = ContainerI()
        identidad = broker.stringToIdentity("Container"+broker.getProperties().getProperty("ContainerNumber"))

        adapter.add(servant, identidad)

        adapter.activate()
        self.shutdownOnInterrupt()

        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(ServerContainer().main(sys.argv))
