#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
Ice.loadSlice('--all comunication.ice')
import drobots
import comunication

class DetectionScannerI(comunication.DetectionScanner):
    def __init__(self, direccion, aperturaEscaner, numeroEncontrado):
        self.direccion = direccion
        self.aperturaEscaner = aperturaEscaner
        self.numeroEncontrado = numeroEncontrado