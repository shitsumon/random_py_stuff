#!/usr/bin/python

class rgb2hsv(object):
	def __init__(self, red, green, blue):
		self.rgb = {}
		self.hsv = {}
		self.rgb = {'red': float(red), 'green': float(green), 'blue': float(blue)}
		self.hsv = {'hue': 0.0, 'saturation': 0.0, 'value': 0.0}

		self.maxValue = float(max(self.rgb['red'], self.rgb['green'], self.rgb['blue']))
		self.minValue = float(min(self.rgb['red'], self.rgb['green'], self.rgb['blue']))

	def convertValue(self):
		if self.maxValue == self.minValue and self.rgb['red'] == self.rgb['green'] == self.rgb['blue']:
			return 0
		elif self.maxValue == self.rgb['red']:
			return 60.0*(float(self.rgb['green'] - self.rgb['blue']) / float(self.maxValue - self.minValue))
		elif self.maxValue == self.rgb['green']:
			return 60.0*(2.0+(float(self.rgb['blue'] - self.rgb['red']) / float(self.maxValue - self.minValue)))
		else:
			return 60.0*(4.0+(float(self.rgb['red'] - self.rgb['green']) / float(self.maxValue - self.minValue)))

	def calculateHue(self):
		if self.convertValue() < 0.0:
			self.hsv['hue'] = self.convertValue() + 360.0
		else:
			self.hsv['hue'] = self.convertValue()

	def calculateSaturation(self):
		if self.maxValue == 0 and self.rgb['red'] == self.rgb['green'] == self.rgb['blue'] == 0:
			self.hsv['saturation'] = 0.0
		else:
			self.hsv['saturation'] = (float(self.maxValue - self.minValue) / float(self.maxValue))

	def calculateValue(self):
		self.hsv['value'] = self.maxValue

	def convertRGB(self):
		self.calculateHue()
		self.calculateSaturation()
		self.calculateValue()
		return self.hsv
