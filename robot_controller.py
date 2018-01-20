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

from detector_warning import *
from detecciones_escaneo import *
from objective import *

class OffensiveController(comunication.OffensiveController, comunication.Estado):
    
    def __init__(self, bot, id, containerNumber, current):

        self.bot = bot
        self.robot_id = id
        self.containerNumber = containerNumber
        self.driving = False
        self.destroyed = False
        self.objetivos = []
        self.resetObjetivos = 0
        self.targets = []
        self.estados = []
        self.contadorMovimiento = 0
        self.litricidad = 100
        print("--- ROBOT ATACKER---")

    def turn(self, current):

        location = self.bot.location()
        self.litricidad -= 1

        if self.destroyed == False:
            if self.driving == False and self.contadorMovimiento == 0:
                self.direccion = random.randint(0, 359)
                self.bot.drive(self.direccion, 100)
                self.driving = True
            elif self.contadorMovimiento != 35 and self.driving == True:
                self.contadorMovimiento += 1
                wide = random.randint(5,20)

            if self.contadorMovimiento == 35:
                self.direccion = random.randint(0,359)
                self.bot.drive(self.direccion,100)
                print("Cambiando direccion de movimiento -> {}".format(self.direccion))


        self.contadorMovimiento += 1
        
        estadoActual = Estado(self.robot_id, location)
        self.sendStatus(estadoActual, self.containerNumber, current)
        
        print("Turn of {} at location {},{}".format(
        id(self), location.x, location.y))

        if len(self.objetivos) > 0:
            print("Intentando disparar...")
            for i in self.objetivos:
                self.targets.append(self.markTarget(self.objetivos.pop(objetivoSeleccionado), location))

        if len(self.targets) > 0:
            self.selectTarget(self.targets)
        
        self.resetObjetivos += 1

        if self.resetObjetivos == 10:
            print("Reseteando objetivos y esas movidas")
            self.objetivos = []
            self.targets = []
            self.resetObjetivos = 0
            """
            try:
                self.bot.cannon(random.randint(0, 359), random.randint(80,120))
            except Exception as e:
                print("Sin energia para disparar // Reseteando objetivos")
			"""

    def selectTarget(self, listaTargets):
        print("Vueno poz vamus a disparar o que? Xd Xd")
        for aliado in self.estados:
            for scope in listaTargets:
                distanciaTargetAliado = math.sqrt(((scope.puntoFinal.x-aliado.location.x)**2)+((scope.puntoFinal.y-aliado.location.y)**2))
                if distanciaTargetAliado > 40:
                    for i in listaTargets:
                        if i.prioridad == 3:
                            self.destroyAnything(i)
                            scope = random.randint(0, len(listaTargets) - 1)
                            self.destroyAnything(listaTargets[scope])

    def destroyAnything(self, objetivo, current=None):
        try:
            print("Un tirito en el pie no?")
            self.bot.cannon(objetivo.direccion, objetivo.distancia)
        except Exception as e:
            print(e)
            print("Energia insuficiente para efectuar el ataque, esperando recarga")
    
    def markTarget(self, direccionEscaner ,posicionOffensive, current=None):
        target = ObjectiveI(direccionEscaner, posicionOffensive, None, 1)
        return target

    def robotDestroyed(self, current=None): ###################### TO DO ###########################
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
                
            elif(proxyAux.ice_isA("::comunication::OffensiveController")):
                print("Enviando estado a todos mi compañeros")
                robot = comunication.SeeingControllerPrx.uncheckedCast(proxy_list[i])
                robot.agregarEstado(estado.id, estado.location)
                

    def receiveObjectives(self, objetivo, current=None):
        for i in self.objetivos:
            if i != objetivo:
                self.objetivos.append(objetivo)
                print("Objetivo recibido -> {}".format(objetivo))
            else:
                print("Objetivo repetido")

    def receiveAlert(self, aviso, current):
        localizacion = self.bot.location()
        target = ObjectiveI(0, localizacion, aviso.location, 3)
        self.targets.append(target)
        
    def agregarEstado(self, id, location, current=None):
        estadoParaAgregar = Estado(id, location)
        self.estados.append(estadoParaAgregar)

class SeeingController(comunication.SeeingController, comunication.Estado):
    
    def __init__(self, bot, id, containerNumber, current):

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
            elif self.contadorMovimiento != 35 and self.driving == True:
                self.contadorMovimiento += 1
                wide = random.randint(5,20)

                for angle in [0,45,90,135,180,225,270,315]:                    
                    localizados = self.bot.scan(angle, wide)
                    print("Escaneando en angulo -> {}, robots localizados -> {}".format(angle, localizados))
                    if localizados > 0:
                        deteccion = DetectionScannerI(angle, wide, localizados)
                        listaEscaner.append(deteccion)
            
                    elif self.contadorMovimiento == 35:
                        self.direccion = random.randint(0,359)
                        self.bot.drive(self.direccion,100)
                        print("Cambiando direccion de movimiento -> {}".format(self.direccion))

        listaObjetivos = []

        if len(listaEscaner) > 0:
            listaObjetivos = self.checkPosition(self.estados, listaEscaner, location)

        if len(listaObjetivos) > 0:
            self.sendObjetives(listaObjetivos, current)


    def checkPosition(self, listaEstadosCompas, listaEscaner, localizacionEscaner):
        contadorCompadresEnEscaner = 0
        listaObjetivos = []
        dx = 0
        dy = 0
        direccionEscanerCompadre = 0
        for i in listaEscaner:
            for j in listaEstadosCompas:
                locationCompadre = j.location
                locationSeeingBot = localizacionEscaner
                dx = locationCompadre.x - locationSeeingBot.x
                dy = locationCompadre.y - locationSeeingBot.y
                direccionEscanerCompadre = math.atan2(dy,dx)

                if direccionEscanerCompadre != i.direccion:
                    listaObjetivos.append(i.direccion)

        return listaObjetivos


    def robotDestroyed(self, current=None):
        self.destroyed = True
        """
        Pending implementation:
        void robotDestroyed();
        """
        print("Os he fallado, lo siento...")

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
            
            elif(proxyAux.ice_isA("::comunication::OffensiveController")):
                print("Enviando estado a todos mi compañeros")
                robot = comunication.OffensiveControllerPrx.uncheckedCast(proxy_list[i])
                robot.agregarEstado(estado.id, estado.location)
                
    def sendObjetives(self, listaObjetivos, current):
        print("Enviando Objetivos...")
        container_prx = current.adapter.getCommunicator().stringToProxy("Container"+self.containerNumber)
        container = services.ContainerPrx.checkedCast(container_prx)
        proxy_list = list(container.list().values())

        for i in  range(len(proxy_list)):
            proxyAux = proxy_list[i]
            if(proxyAux.ice_isA("::comunication::OffensiveController")):
                print("Aqui Alfa Tango Charlie {}, preparen armas".format(self.robot_id))
                robot = comunication.OffensiveControllerPrx.uncheckedCast(proxyAux)
                print("Enviando Objetivos")
                for j in listaObjetivos:
                    robot.receiveObjectives(j) 

    def agregarEstado(self, id, location, current=None):
        estadoParaAgregar = Estado(id, location)
        self.estados.append(estadoParaAgregar)
    """
    def manageAlert(self, warning, current):

        shoot = True
        for est in self.estados:
            if(est.location == warning.location):
                shoot = False

        if(shoot):
            container_prx = current.adapter.getCommunicator().stringToProxy("Container"+self.containerNumber)
            container = services.ContainerPrx.checkedCast(container_prx)
            proxy_list = list(container.list().values())
            
            for i in range(len(proxy_list)):
                proxyAux = proxy_list[i]
                if(proxyAux.ice_isA("::comunication::OffensiveController")):
                    robot = comunication.OffensiveControllerPrx.uncheckedCast(proxyAux)
                    print("Enviando Objetivos")
                    puntico = warning.location
    """                 

class Estado():

    def __init__(self, id, location):
        self.id = id
        self.location = location
        
    def getLocation(self): #################################################### QUIT METHOD
        return self.location

