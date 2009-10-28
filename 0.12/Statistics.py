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

0.10 2009-04-16 Initial version.
0.23 2009-09-15 Version updated with new API redesigned.
'''

"""

:mod:`Statistics` -- statistical structure module
==========================================================================

This module have the class which is responsible to keep the statistics of 
the PSO. This is  the main class which must BE INHERITED by the other statistic
dump classes

"""


import Consts


class Statistics(object):
	""" Statistics Class - A class bean-like to store the statistics
		This class must be INHERITED by other statistics classes.
		
		Example:
			>>> stats = pso_engine.getStatistics()
			>>> st["fitMax"] 
			10.2
	"""
	#'fit' means 'fitness'
	def __init__(self):
		self.internalDict = {}
		self.descriptions = {}
        
	def __getitem__(self,key):
		""" Returtn the specific statistic by key """
		return self.internalDict[key]
    
	def __setitem__(self,key,value):
		""" Set the statistic """	
		self.internalDict[key] = value

	def __len__(self):
		""" Return the lenght of internal stats dictionary """
		return len(self.internalDict)
	

	def __repr__(self):
		"""Return a string representation of the statistics"""
		strBuff = "-Statistics\n"
		for k,v in self.internalDict.items():
			strBuff += "\t%-45s = %.2f\n" % (self.descriptions.get(k,k), v)
		return strBuff
     
	def asTuple(self):
		"""Return a string representation of the statistics"""
		return tuple(self.internalDict.values())

	def clear(self):
		"""Clear the statistics dictionary"""
		for k in self.internalDict.keys():
			self.internalDict[k] = 0

	def items(self):
		"""Return a tuple (name,value) for all stored statistics"""
		return self.internalDict.items()