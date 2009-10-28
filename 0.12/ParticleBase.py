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
0.20 2009-05-21 Added support for Local Communicator (ownLocalBestPosition and ownLocalBestFitness)
0.23 2009-08-29 Changed all code for support a better generalization. Particle is now BaseParticle.py
'''


"""
:mod:`ParticleBase` -- the particles base module
================================================================

    This module have the class which every particle of the swarm extends,
    If you are planning to create a new representation, you must take a
    inside look into this module.
"""

from FunctionSlot import FunctionSlot

class ParticleBase(object):
	"""ParticleBase Class - the base of all particle representation """
	
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
	
	

	def __init__(self):
		""" Particle Constructor """
		self.evaluator = FunctionSlot("Evaluator")
		self.position_initializator = FunctionSlot("Position Initializator")
		self.velocity_initializator = FunctionSlot(" Velocity Initializator")
		self.position_communicator = FunctionSlot("Position Communicator")
		self.information_communicator = FunctionSlot("Information Communicator")
		
		self.allSlots = [self.evaluator, self.position_initializator,
					self.velocity_initializator, self.position_communicator, self.information_communicator]
		
		self.internalParams = {}
		self.fitness = 0.0
		self.ownBestFitness = 0.0
		
	def getFitness(self):
		""" Get the Fitness Score of the particle"
		
		:rtype particle fitness score
		
		"""
		return self.fitness
	
	def getOwnBestFitness(self):
		"""Get the best Fitness score of the particle
		
		:rtype particle best fitness score
		"""
		
		return self.ownBestFitness
	
	def __repr__(self):
		""" String representation of the Particle"""
		ret = "- ParticleBase\n"
		ret += "\tFitness:\t\t\t %.6f\n" %(self.fitness,)
		ret += "\tOwnBestFitness:\t\t\t %.6f\n" %(self.ownBestFitness,)
		ret += "\tInit Params:\t\t %s\n\n" %(self.internalParams,)
		for slot in self.allSlots:
			ret += "\t"+ slot.__repr__()
		ret += "\n"
		
		return ret
	
	def setOwnBestFitness(self,fitness):
		""" Set the best fitness of the particle 
			
			:param fitness: the best fitness of the particle
		"""
		
		self.ownBestFitness = fitness
	
	
	def setParams(self, **args):
		"""Set the initializator params"
		
		Example:
			>>> particle.setParams(rangemin=0, rangeMax=100,dimmensions=4)
		
		:param args: this params will saved in every particle for swarm op. use
		
		"""
		self.internalParams.update(args)
	
	def getParam(self,key,nvl=None):
		""" Gets an initialization parameter
		
		Example:
			>>> particle.getParam("rangemax")
			100
		
		:param key: the key of parma
		:param nvl: if the key doesn't exist, the nvl will be returned
		
		"""
		return self.internalParams.get(key,nvl)	


	def resetStats(self):
		"""Clear fitness of the particle """
		self.fitness = 0.0
	
	def evaluate(self, **args):
		""" Called to evaluate the particle
		
		:param args: these parameters will be passed to the evaluator
		"""
		self.resetStats()
		for it in self.evaluator.applyFunctions(self, **args):
			self.fitness += it
		
	def initializePosition(self, **args):
		"""Called to initialize the particle position
		
		:param args: these parameters will be passed to the initializator
		
		"""
		for it in self.position_initializator.applyFunctions(self, **args):
			pass
	
	
	def initializeVelocity(self, **args):
		"""Called to initialize the particle velocity
		
		:param args: these parameters will be passed to the initializator
		
		"""
		for it in self.velocity_initializator.applyFunctions(self,**args):
			pass

	def copy(self, other):
		""" Copy the current GenomeBase to 'g'
		
		:param other: the destination particle      

		"""
		other.fitness = self.fitness
		other.ownBestFitness = self.ownBestFitness
		other.evaluator = self.evaluator
		other.position_initializator = self.position_initializator
		other.velocity_initializator = self.velocity_initializator
		other.position_communicator = self.position_communicator
		other.information_communicator = self.information_communicator
		other.allSlots = self.allSlots[:]
		other.internalParams = self.internalParams.copy()
		

	def clone(self):
		""" Clone this ParticleBase
		
		:rtype: the clone particle
		
		"""
		
		newcopy = ParticleBase()
		self.copy(newcopy)
		return newcopy
		
		