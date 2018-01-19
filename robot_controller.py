#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
Ice.loadSlice('--all services.ice')
import services
Ice.loadSlice('--all comunication.ice')
import comunication
import math
import random

class OffensiveController(comunication.OffensiveController, comunication.Estado):
    
    def __init__(self, bot, id, containerNumber, current=None):
    	
        self.bot = bot
        self.robot_id = id
        self.containerNumber = containerNumber
        self.driving = False
        self.destroyed = False
        self.objetivos = []
        print("--- ROBOT ATACKER---")

    def turn(self, current):

        location = self.bot.location()
        estadoActual = Estado(self.robot_id, location)
        self.sendStatus(estadoActual, self.containerNumber, current)
        
        print("Turn of {} at location {},{}".format(
            id(self), location.x, location.y))

        if len(self.objetivos) > 0:
            objetivoSeleccionado = random.randint(0, self.objetivos.len()-1)
            self.destroyAnything(self.objetivos.pop(objetivoSeleccionado))

        self.objetivos = []

        

    def destroyAnything(self, objetivo ,current=None):
        try:
            self.bot.cannon(objetivo.getDireccion(), objetivo.getDistancia())
        except NoEnoughEnergy as e:
            print("Energia insuficiente para efectuar el ataque, esperando recarga")
    
    def ola(self, direccion, distancia ,current=None):
        try:
            self.bot.cannon(direccion, distancia)
        except Exception as e:
            print("Energia insuficiente para efectuar el ataque, esperando recarga")

    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        print("Recordarme como un heroe...") 

    def sendStatus(self, estado, containerNumber, current):
        print("Enviando estado")
        container_prx = current.adapter.getCommunicator().stringToProxy("Container"+containerNumber)
        container = services.ContainerPrx.checkedCast(container_prx)
        proxy_list = list(container.list().values())

        for i in  range(len(proxy_list)):
            proxyAux = proxy_list[i]
            if(proxyAux.ice_isA("::comunication::SeeingController")):
                print("Enviando estado a todos mi compañeros")
                robot = comunication.SeeingControllerPrx.uncheckedCast(proxy_list[i])
                robot.agregarEstado(estado.id, estado.location)	

    def receiveObjectives(self, listaObjetivos, current):
        for i in listaObjetivos:
            self.objetivos.append(i)
            print("Objetivo recibido")

class SeeingController(comunication.SeeingController, comunication.Estado):
    
    def __init__(self, bot, id, containerNumber, current=None):
        self.bot = bot
        self.robot_id = id
        self.containerNumber = containerNumber
        self.driving = False
        self.destroyed = False
        self.estados = []
        self.contadorMovimiento = 0
        self.direccion = 0
        print("--- ROBOT DEFENDER ---")

    def turn(self, current):
        """
        Method that will be invoked remotely by the server. In this method we
        should communicate with out Robot
        """
        listaEscaner = []
        location = self.bot.location()
        estadoActual = Estado(self.robot_id, location)
        self.sendStatus(estadoActual, self.containerNumber, current)

        print("Turn of {} at location {},{}".format(
            id(self), location.x, location.y))

        if self.destroyed == False:
            if self.driving == False and self.contadorMovimiento == 0:
                self.direccion = random.randint(0, 359)
                self.bot.drive(self.direccion, 100)
                self.driving = True
            elif self.contadorMovimiento != 5 and self.driving == True:
                self.contadorMovimiento += 1
                wide = random.randint(5,20)

                for angle in [0,45,90,135,180,225,270,315,359]:                    
                    localizados = self.bot.scan(angle, wide)
                    
                    if localizados > 0:
                        deteccion = deteccionesEscaneo(angle, wide, localizados)
                        listaEscaner.append(deteccion)
            
            elif self.contadorMovimiento == 5:
                self.direccion = random.randint(0,359)
                self.bot.drive(self.direccion,100)

            if len(listaEscaner) > 0:
                listaObjetivos = self.checkPosition(self.estados, listaEscaner, location)


    def checkPosition(self, listaEstadosCompas, listaEscaner, localizacionEscaner):
        contadorCompadresEnEscaner = 0
        listaObjetivos = []
        dx = 0
        dy = 0
        direccionEscanerCompadre = 0
        for i in listaEscaner:
            for j in listaEstadosCompas:
                locationCompadre = j.getLocation()
                locationSeeingBot = localizacionEscaner
                dx = locationCompadre.x - locationSeeingBot.x
                dy = locationCompadre.y - locationSeeingBot.y
                direccionEscanerCompadre = math.atan2(dy,dx)

                if direccionEscanerCompadre != i.getDireccion():
                    objetivoNuevo = objetivo(i.getDireccion(), locationSeeingBot)
                    listaObjetivos.append(objetivoNuevo)

        return listaObjetivos


    def robotDestroyed(self, current):
        self.destroyed = True
        """
        Pending implementation:
        void robotDestroyed();
        """
        print("Os he fallado, lo siento...")

    def sendStatus(self, estado, containerNumber, current=None):
        print("Enviando estado")
        container_prx = current.adapter.getCommunicator().stringToProxy("Container"+containerNumber)
        container = services.ContainerPrx.checkedCast(container_prx)
        proxy_list = list(container.list().values())

        for i in  range(len(proxy_list)):
            proxyAux = proxy_list[i]
            if(proxyAux.ice_isA("::comunication::SeeingController")):
                print("Enviando estado a todos mi compañeros")
                robot = comunication.SeeingControllerPrx.uncheckedCast(proxy_list[i])
                robot.agregarEstado(estado.id, estado.location)
            
    def sendObjetives(self, listaObjetivos, containerNumber, current=None):
        print("Enviando Objetivos...")
        container_prx = current.adapter.getCommunicator().stringToProxy("Container"+containerNumber)
        container = services.ContainerPrx.checkedCast(container_prx)
        proxy_list = list(container.list().values())

        for i in  range(len(proxy_list)):
            proxyAux = proxy_list[i]
            if(proxyAux.ice_isA("::comunication::OffensiveController")):
                print("Aqui Alfa Tango Charlie {}, preparen armas".format(self.robot_id))



    def agregarEstado(self, id, location, current):
        estadoParaAgregar = Estado(id, location)
        self.estados.append(estadoParaAgregar)

class Estado():
    def __init__(self, id, location):
        self.id = id
        self.location = location

    def getLocation(self):
        return self.location

class deteccionesEscaneo():
    def __init__(self, direccion, aperturaEscaner, numeroEncontrado):
        self.direccion = direccion
        self.aperturaEscaner = aperturaEscaner
        self.numeroEncontrado = numeroEncontrado

    def getDireccion(self):
        return self.direccion

    def getNumeroEncontrado(self):
        return self.numeroEncontrado

class objetivo():
    def __init__(self, direccion, puntoInicialEscaner):
        self.direccion = direccion
        self.distancia = self.calcularDistancia(direccion, puntoInicialEscaner)

    def calcularDistancia(self, direccion, puntoInicialEscaner):
        puntoFinalEscaneo = [int(399 * (math.sin(direccion))),int(399 * math.cos(direccion))]

        if puntoFinalEscaneo[1] < 0:
            puntoFinalEscaneo[1] = 0
        elif puntoFinalEscaneo[1] > 399:
            puntoFinalEscaneo[1] = 399
        elif puntoFinalEscaneo[0] < 0:
            puntoFinalEscaneo[0] = 0
        elif puntoFinalEscaneo[0] > 399:
            puntoFinalEscaneo[0] = 399

        distanciaX = puntoFinalEscaneo[1]-puntoInicialEscaner.x
        distanciaY = puntoFinalEscaneo[0]-puntoInicialEscaner.y

        distancia = math.sqrt(((distanciaX**2)+(distanciaY**2)))

        return (distancia/2)
