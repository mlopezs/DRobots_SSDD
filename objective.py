#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
Ice.loadSlice('--all comunication.ice')
import comunication
import math

class ObjectiveI(comunication.Objective):

    def __init__(self, direccionEscaner, posicionOffensive, puntoFinalDeAlerta, prioridad):
        
        if puntoFinalDeAlerta != 0:
            self.puntoFinal = puntoFinalDeAlerta
        else:
            self.puntoFinal = calcularPuntoFinal(direccionEscaner)
            
        self.prioridad = prioridad
        self.distancia = self.calcularDistancia(self.puntoFinal, posicionOffensive)
        self.direccion = self.calcularDireccion(self.distancia,self.puntoFinal, posicionOffensive)
        

    def calcularDistancia(self, puntoFinal, puntoInicial):
        distanciaX = puntoFinal.x-puntoInicial.x
        distanciaY = puntoFinal.y-puntoInicial.y

        distancia = math.sqrt(((distanciaX**2)+(distanciaY**2)))
        print("Para una distancia de: {}".format(distancia))

        if self.prioridad != 3:
            return (distancia/2)
        else:
            return(distancia)

    def calcularDireccion(self, hipotenusa, puntoFinal, posicionOffensive):
        cat = puntoFinal.x - posicionOffensive.x
        angulo = 1/(math.cos(cat/hipotenusa))

        if posicionOffensive.x > puntoFinal.x and posicionOffensive.y < puntoFinal.y:
            angulo += 90
        elif posicionOffensive.x > puntoFinal.x and posicionOffensive.y > puntoFinal.y:
            angulo += 180
        elif posicionOffensive.x < puntoFinal.x and posicionOffensive.y > puntoFinal.y:
            angulo += 270
            
        return angulo

    def calcularPuntoFinal(self, direccionEscaner):
        puntoFinal = drobots.Point(x=int(399 * (math.sin(direccionEscaner))), y=int(399 * math.cos(direccionEscaner)))

        if puntoFinal.y < 0:
            puntoFinal.y = 0
        elif puntoFinal.y > 399:
            puntoFinal.y = 399
        elif puntoFinal.x < 0:
            puntoFinal.x = 0
        elif puntoFinal.x > 399:
            puntoFinal.x = 399

        print("Direccion: {} \tPunto final del escaneo -> {}".format(direccionEscaner,puntoFinal))
        return puntoFinal
