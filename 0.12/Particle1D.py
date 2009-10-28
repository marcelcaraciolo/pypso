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

0.10 2009-09-02 Initial version.
'''


"""
:mod:`Particle1D` -- the 1D list particle
================================================================

    This is the 1D List representation, this list can carry real numbers
	or integers or any kind of object. This particle class extends the :class:`ParticleBase.ParticleBase` class.

"""

from ParticleBase import ParticleBase
import Consts

class Particle1D(ParticleBase):
	""" Particle1D Class - The 1D List particle representation
	
	**Example**
	
		The instantiation
			>>> g = Particle1D(6)
			
	:param size: the 1D list size

	"""

	evaluator = None
	""" This is the :term 'evaluator function' slot, you can add a function with
	the *set* method: ::
	
		particle.evaluator.set(eval_func)
	"""
	
	position_initializator = None
	""" This is the position initialization function of the particle, you can change
	the default initializator using the function slot: :: 
		
		particle.position_initializator.set(Initializator.G1DListInitializatorDimmension)
	
	In this example, the initializator: func:`Initializators.G1DListInitializatorDimmension``
	will be used to create the initial position of the particle..
		
	  """

	velocity_initializator = None
	""" This is the velocity initialization function of the particle, you can change
	the default initializator using the function slot: :: 
		
		particle.velocity_initializator.set(Initializator.G1DListInitializatorDimmension)
	
	In this example, the initializator: func:`Initializators.G1DListInitializatorDimmension``
	will be used to create the initial velocity of the particle..
		
	 """
	
	position_communicator = None
	""" This is the position communication function slot, you can change the default
	communicator using the slot *set* function: ::
	
	particle.position_communicator.set(Communicators.P1DGlobalPosCommunicator)
	
	"""
	information_communicator = None
	""" This is the information communication function slot, you can change the default
	communicator usingt the slot *set* function: ::
	
	particle.information_communicator.set(Communicators.P1DGlobalInfoCommunicator)
	"""
	
	
	def __init__(self,size):
		""" The initializator of Particle1D representation,
		size parameter must be specified """
		ParticleBase.__init__(self)
		self.position = []
		self.ownBestPosition = []
		self.velocity = []
		self.dimmensionsSize = size
		self.position_initializator.set(Consts.CDefP1DPosListInit)
		self.velocity_initializator.set(Consts.CDefP1DVelListInit)
		self.position_communicator.set(Consts.P1DPosCommunicator)
		self.information_communicator.set(Consts.P1DInfoCommunicator)
	
	def __eq__(self, other):
		""""Compares one particle with another """
		cond1 = (self.position == other.position) 
		cond2 = (self.dimmensionsSize == other.dimmensionsSize)
		cond3 = (self.velocity == other.velocity)
		cond4 = (self.ownBestPosition) == (other.ownBestPosition)
		return True if cond1 and cond2 and cond3 and cond4 else False

	
	def getVelocity(self):
		""" Return the current velocity of the particle """
		return self.velocity
	
	def getPosition(self):
		""" Return the  current position of the particle """
		return self.position

	def getOwnBestPosition(self):
		""""Return the current best position of the particle """
		return self.ownBestPosition
		
	
	def setOwnBestPosition(self,position):
		""" Set the best position of the particle 
			
			:param position: the best position of the particle
		"""
			
		self.ownBestPosition = position[:]

		
	def __len__(self):
		""""Return the size of dimmensions particle """
		return self.dimmensionsSize


	def __repr__(self):
		""""Return a string representation of the Particle """
		ret = ParticleBase.__repr__(self)
		ret += "-Particle1D\n"
		ret += "\tDimmensions size:\t %s\n" % (self.dimmensionsSize,)
		#ret += "\tPosition:\t\t %s\n\n" %(self.position,)
		ret += "\tBestPosition:\t\t %s\n\n" %(self.ownBestPosition,)
		return ret
	

	def clearAll(self):
		""" Remove all elements from Velocity and Position """
		del self.position[:]
		del self.velocity[:]
		del self.ownBestPosition[:]
	
	def clearList(self,typed):
		""" Remove all specified lists from Particle
			Example:
				>>> particle.clearList('position')'
			
			:param typed: the list attribute that will be removed. ('position' or 'velocity')'
			
		"""
		if typed == 'position':
			del self.position[:]
			del self.ownBestPosition[:]
		elif typed == 'velocity':
			del self.velocity[:]
			
	
	def append(self, typed, value):
		""" Appends an item to the list
			Example:
				>>> particle.append('position', 44)
			
			:param typed: The list attribute that will be appended. ('position' or 'velocity')
			:param value: value to be added
		
		"""
		
		if typed == "position":
			self.position.append(value)
			self.ownBestPosition.append(value)
		elif typed == 'velocity':
			self.velocity.append(value)
	
	def copy(self, g):
		"""Copy particle to 'g''
		Example:
			>>> particle_origin.copy(particle_destination)
		
		:param g: the destination Particle1D instance
		
		"""
		ParticleBase.copy(self,g)
		g.dimmensionsSize = self.dimmensionsSize
		g.velocity = self.velocity[:]
		g.position = self.position[:]
		g.ownBestPosition = self.ownBestPosition[:]

	def clone(self):
		""" Return a new instance copy of the particle
		
		:rtype: The Particle1D clone instance
		
		"""
		newcopy = Particle1D(self.dimmensionsSize)
		self.copy(newcopy)
		return newcopy