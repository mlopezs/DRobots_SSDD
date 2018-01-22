#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all communication.ice')
import communication

class DetectionScannerI(communication.DetectionScanner):

    def __init__(self, direccion, aperturaEscaner, numeroEncontrado):
        
        self.direccion = direccion
        self.aperturaEscaner = aperturaEscaner
        self.numeroEncontrado = numeroEncontrado