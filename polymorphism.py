#!/usr/bin/python

"""
Copyright (c) 2014 Michael Flau <michael@flau.net>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

"""
Simple example how to use Polymorphism and Introspection
in Python to create a Factory like interface to a subset of concrete
classes derived from the same abstract base class.
"""

import abc

#Abstract base class
class AbstractAnimal(object):

	__metaclass__ = abc.ABCMeta
	classname = "AbstractAnimal"	

	@abc.abstractmethod
	def __init__(self):
		pass

	@abc.abstractmethod
	def makeSound(self):
		"""Sound of an animal"""
		return

	def getName(self):
		return self.classname

#Concrete class 1
class Dog(AbstractAnimal):

	#classname = "Dog"

	def __init__(self):
		setattr(self, "classname", "Dog")
		#pass

	def makeSound(self):
		print "The dog makes Wuff Wuff!"

#Concrete class 2
class Cat(AbstractAnimal):

	#classname = "Cat"

	def __init__(self):
		setattr(self, "classname", "Cat")
		#pass

	def makeSound(self):
		print "The cat makes Mew Mew!"

#Concrete class 3
class Parrot(AbstractAnimal):

	#classname = "Parrot"

	def __init__(self):
		setattr(self, "classname", "Parrot")
		#pass

	def makeSound(self):
		print "The parrot makes Rrraaahh Rrraaahh!"

#Class which uses the
#animal classes to show Polymorphism
class AnimalSoundbox(object):

	def __init__(self):
		pass

	def rattleTheBox(self,animal):
		animal.makeSound()

#Interface class for convenient
#instantiation of animals
class iAnimalMaker(object):

	classlist = []

	def __init__(self):

		self.classlist = AbstractAnimal.__subclasses__()
		return

	def createAnimal(self, animalname):
		for subclass in self.classlist:
			if subclass().getName() == animalname:
				return subclass()
		
		print "No class with that name found!"
		return -1




if __name__ == "__main__":

	animalFactory = iAnimalMaker()

	animals = []

	animals.append(animalFactory.createAnimal("Dog"))
	animals.append(animalFactory.createAnimal("Cat"))
	animals.append(animalFactory.createAnimal("Parrot"))
	animals.append(animalFactory.createAnimal("Parrot"))
	animals.append(animalFactory.createAnimal("Dog"))
	animals.append(animalFactory.createAnimal("Whale")) #Provoke Error

	box = AnimalSoundbox() 

	for animal in animals:

		if not animal == -1:
			box.rattleTheBox(animal)
		else:
			print "Item is no animal!"

