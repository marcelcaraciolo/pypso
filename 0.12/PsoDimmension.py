'''
Particle Swarm Optimization - PyPSO 

Copyright (c) 2009 Marcel Pinheiro Caraciolo
caraciol@gmail.com

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

0.10 2009-09-30 Initial version.
'''


"""

:mod:`PsoDimmension` -- the particle dimmensions module
===========================================================

In this module, there are the :class:`PsoDimmension.PsoDimmensions` class (which is the
class that holds the dimmension types) to use with the supported particles.

"""

import random
import Consts

class PsoDimmensions(object):
	""" PsoDimmensions Class - the set of dimmensions
	
	Example:
		>>> position = PsoDimmensions()
		>>> choices = [1,2,3,4]
		>>> lst = DimmensionList(choices)
		>>> position.add(lst)
		>>> position[0].getRandomDimmension() in lst
		True
		
	param dimmension_list: the list of dimmensions
	param homogeneous: if is True, all the dimmensions will be use only the first added

	"""
	
	def __init__(self, dimmension_list= [], homogeneous= False):
		""" The constructor of PsoDimmensions class """
		self.dimmension_list = []
		self.dimmension_list.extend(dimmension_list)
		self.homogeneous = homogeneous
		
	def add(self, dimmension):
		""" Appends one dimmension to the dimmensions list 
		
		:param dimmension: dimmension to be  added
		
		"""
		self.dimmension_list.append(dimmension)
		
	def __getslice__(self, a, b):
		""" Returns the slice part of dimmensions list """
		return self.dimmensions_list[a:b]
		
	
	def __getitem__(self,index):
		""" Returns the index dimmension of the dimmension list """
		if self.homogeneous: return self.dimmension_list[0]
		try:
			val = self.dimmension_list[index]
		except IndexError:
			Util.raiseException(
			"""An error was ocurred while finding dimmension for the %d position of the particle.
				You may consider use the 'homogeneous''parameter of the PsoDimmensions class""" % (index,))
		
		return val
	
	def __setitem__(self,index, value):
		"""Sets the index dimmension of the dimmension list """ 
		if self.homogeneous: self.dimmension_list[0] = value
		self.dimmension_list[index] = value
	
	
	def __iter__(self):
		"""Return the list iterator """
		if self.homogeneous:
			oneList = [self.dimmension_list[0]]	
			return iter(oneList)
		return iter(self.dimmension_list)
	
	
	def __len__(self):
		"""Returns the length of the dimmensions list """
		if self.homogeneous: return 1
		return len(self.dimmension_list)
		
	def __repr__(self):
		""" Return a string representation of the dimmension """
		ret = "-Dimmensions\n"
		ret += "\tHomogeneous:\t %s\n" % (self.homogeneous,)
		ret += "\tList Size:\t %s\n" %(len(self),)
		ret += "\tDimmensions:\n\n"
		if self.homogeneous:
			ret += "Dimmension for 0 position:\n"
			ret += self.dimmension_list[0].__repr__()
		else:
			for i in xrange(len(self)):
				ret += "Dimmension for %d position:\n" %(i,)
				ret += self.dimmension_list[i].__repr__()
		
		return ret
		
		
class DimmensionList(object):
	"""DimmensionList Class - The list dimmension type
	
	Example:
		>>> position = PsoDimmensions()
		>>> choices = [1,2,3,4]
		>>> lst = DimmensionList(choices)
		>>> position.add(lst)
		>>> position[0].getRandomDimmension() in lst
		True
	"""
	
	def __init__(self, options =[]):
		""" The cosntructor of DimmensionList class """
		self.options = []
		self.options.extend(options)
		
	def clear(self):
		""" Removes all the dimmension options from the list """
		del self.options[:]
	
	def getRandomDimmension(self):
		"""Returns one random choice from the options list """
		return random.choice(self.options)
		
	
	def add(self,option):
		"""Appends one option to the options list
		
		:param option: option to be added in the list
 		"""
		self.options.append(option)
		
	
	def __getslice__(self, a, b):
		"""Returns the slice part of options """
		return self.options[a:b]
		

	def __getitem__(self,index):
		""" Returns the index option of the options list """
		return self.options[index]

	def __setitem__(self,index, value):
		"""Sets the index option of the list """ 
		self.options[index] = value


	def __iter__(self):
		"""Return the list iterator """
		return iter(self.optionss)

	def __len__(self):
		"""Returns the length of the options list 
		"""
		return len(self.options)


	def remove(self, option):
		""" Removes the option from list 
			
		:param option: remove the option from the list
		
		"""
		self.options.remove(option)
		
		
	def __repr__(self):
		""" Return a string representation of the dimmension """
		ret = "-DimmensionList\n"
		ret += "\tList Size:\t %s\n" %(len(self),)
		ret += "\Dimmension Options:\t %s\n\n" % (self.options,)
		return ret
		

class DimmensionRange(object):
	""" DimmensionRange Class - the range dimmension type
	
	Example:
		>>> ranges = DimmensionRange(0,100)
		>>> ranges.getRandomDimmension() >= 0 and ranges.getRandomDimmension() <= 100
		True
		
	:param begin: the begin of the range
	:param end: the end of the range
	:param real: if True, the range will be of real values
	
	"""
	
	def __init__(self,begin=0,
				end=100, real= False):
		"""The constructor of DimmensionRange class """
		self.beginEnd = [(begin,end)]
		self.real = real
		
	
	def add(self,begin,end):
		""" Add a new range
		
		:param begin: the begin of range
		:paran end: the end of the range
		
		"""
		self.beginEnd.append((begin,end))
		
		
	def clear(self):
		"""Removes all ranges """
		del self.beginEnd[:]
	
	
	def getRandomDimmension(self):
		""" Returns one random choice between the range """
		rand_func = random.uniform if self.real else random.randint
		
		choice = random.randint(0,len(self.beginEnd)-1)
		return rand_func(self.beginEnd[choice][0], self.beginEnd[choice][1])
		
		
	def setReal(self, flag=True):
		"""Sets True if the range is real or False if is Integer
		
		:param flag: True or False
		"""
		self.real = flag
	
	def getReal(self):
		"""Returns True if the range is real or False if is Integer """
		return self.real
	
	
	def __len__(self):
		""" Returns the ranges in the dimmension """
		return len(self.beginEnd)
		
	
	def __repr__(self):
		"""Return a string representation of the dimmension """
		ret = "-DimmensionRange\n"
		ret += "\tReal:\t\t %s\n" % (self.real,)
		ret += "\tRanges Count:\t %s\n" % (len(self),)
		ret += "\tRange List:\n"
		for beg, end in self.beginEnd:
			ret += "\t\t\t Range from [%s] to [%s]\n" % (beg, end)
		ret += "\n"
		return ret

	