#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import sys
import Ice
Ice.loadSlice('--all drobots.ice')
import drobots
import math


class Objective():

	def __init__(self, dirScanner, posAtacante, posObjetivo, prioridad):

		self.prioridad = prioridad
		self.posAtacante = posAtacante
		self.posObjetivo = self.calcularPosicionObjetivo(dirScanner, posObjetivo)
		self.distancia = self.calcularDistancia()
		self.direccion = self.calcularDireccion()

	def calcularDistancia(self):

		disX = self.posObjetivo.x - self.posAtacante.x
		disY = self.posObjetivo.y - self.posAtacante.y

		dist = math.hypot(disX, disY) # math.sqrt(((disX**2)+(disY**2)))

		if !prioridad:
			return dist/2
		else:
			return dist

	def calcularDireccion(self):

		obj_x = self.posObjetivo.x
		obj_y = self.posObjetivo.y
		atck_x = self.posAtacante.x
		atck_y = self.posAtacante.y

		cat = abs(obj_x - atck_x)
		angulo = 1/(math.cos(cat/self.distancia))

		if atck_x > obj_x and atck_y < obj_y:
			angulo += 90
		elif atck_x > obj_x and atck_y > obj_y:
			angulo += 180
		elif atck_x < obj_x and atck_y > obj_y:
			angulo += 270

		return angulo

	def calcularPosicionObjetivo(self, angScan_deg, posObjIni):

		if angScan_deg is None:
			return posObjIni

		angScan_rad = math.radians(angScan_deg)

		atck_x = self.posAtacante.x
		atck_y = self.posAtacante.y
		
		if angScan_deg == 0:
			posObj = drobots.Point(x = 399, y = atck_y)
		elif angScan_deg == 45:
			posObj = drobots.Point(x = 399, y = 399)
		elif angScan_deg == 90:
			posObj = drobots.Point(x = atck_x, y = 399)
		elif angScan_deg == 135:
			posObj = drobots.Point(x = 0, y = 399)
		elif angScan_deg == 180:
			posObj = drobots.Point(x = 0, y = atck_y)
		elif angScan_deg == 225:
			posObj = drobots.Point(x = 0, y = 0)
		elif angScan_deg == 270:
			posObj = drobots.Point(x = atck_x, y = 0)
		elif angScan_deg == 315:
			posObj = drobots.Point(x = 399, y = 0)
		elif angScan_deg in (list(range(0, 45)) + list(range(315, 360))):
			posObj = drobots.Point(x = 399, y = atck_y * ( 1 + math.sin(angScan_rad)))
		elif angScan_deg in range(45, 135):
			posObj = drobots.Point(x = atck_x * ( 1 + math.cos(angScan_rad)), y = 399)
		elif angScan_deg in range(135, 225):
			posObj = drobots.Point(x = 0, y = atck_y * ( 1 + math.sin(angScan_rad)))
		elif angScan_deg in range(225, 360):
			posObj = drobots.Point(x = atck_x * ( 1 + math.cos(angScan_rad)), y = 0)

		return posObj