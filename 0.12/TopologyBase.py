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
0.11 2009-05-25 Added get method getStatistics() for support statitiscs reports.
0.23 2009-09-06 Added support for new API. All redesigned.
'''

"""
:mod:`TopologyBase` -- the topology base  module
================================================================

This module contains the :class:`TopologyBase.TopologyBase` class, which is reponsible
to stablish the information change between the particles.

"""

import Consts
from FunctionSlot import FunctionSlot
import math 
from FloatStatistics import TopologyStatistics
from FloatStatistics import SwarmStatistics


def key_fitness_score(particle):
	""" A key function to return the fitness score
	
	:param particle: the particle instance
	:rtype: the particle fitness
	
	.. note:: this function is used by the max()/min() python functions
	
	"""
	return  particle.fitness

def key_best_fitness_score(particle):
	""" A key function to return the best fitness score, used by max()/min()
	
	:param particle: the particle instance
	:rtype: the particle fitness score
	
	.. note:: This funciton is used by the max()/min() python functions
	
	"""
	return particle.ownBestFitness
	
def cmp_particle_fitness(a,b):
	""" Compares two particle fitness
	
	Example:
		>>> Topology.cmp_particle_fitness(a,b)
	
	:param a: the A particle instance
	:param b: the B particle instance
	:rtype:  0 if the two particles fitness are the same
			 -1 if the B particle fitness is greater than A and
			1 if the A particle fitness is greater than B.
	
	.. note:: this function is used to sort the topology individuals
	
	"""
	if a.fitness < b.fitness: return -1
	if a.fitness > b.fitness: return 1
	return 0


def cmp_particle_bestFitness(a,b):
	""" Compares two particle best fitness, used for sorting the topology
	
	Example:
		>>> Topology.cmp_particle_bestFitness(a,b)
	
	:param a: the A particle instance
	:param b: the B particle instance
	:rtype:  0 if the two particles  best fitness are the same
			 -1 if the B particle best fitness is greater than A and
			1 if the A particle best fitness is greater than B.
	
	.. note:: this function is used to sort the topology individuals
	
	"""
	
	if a.ownBestFitness < b.ownBestFitness: return -1
	if a.ownBestFitness > b.ownBestFitness: return 1
	return 0
	
class TopologyBase(object):
	""" Topology Base Class - The container for the swarm
	
	**Examples**
		Get the swarm from the :class:`PSO.SimplePSO` (PSO Engine) instance
			>>> swarm = pso_engine.getSwarm()
		
		Get the best fitness particle
			>>> bestParticle = swarm.bestFitness()
		
		Ge the statistics from the :class:`Statistics.Statistics` instance
			>>> stats = swarm.getStatistics()
			>>> print stats["fitMax"]
			10.4
		
		Iterate, get/set individuals
			>>> for particle in swarm:
			>>>		print particle
			(...)
			
			>>> for i in xrange(len(swarm)):
			>>>		print swarm[i]
			(...)
			
			>>> swarm[10] = newParticle
			>>> swarm[10].fitness
			12.5
			
	:param particle: the :term: `Sample particle``
	
	"""
	
	position_updater = None
	""" This is the position update topology function slot, you can change the default
	updater using the slot *set* function: ::
	
	topology.position_updater.set(GlobalTopology.GlobalPositionUpdater)
	
	"""
	information_updater = None
	""" This is the information update topology function slot, you can change the default
	updater usingt the slot *set* function: ::
	
	topology.information_communicator.set(GlobalTopology.GlobalInformationUpdater)
	"""
	
	
	def __init__(self,particle):
		""" The Topology Class Creator """
		print "New topology instance, %s class particles." % (particle.__class__.__name__,)
		self.oneSelfParticle = particle
		self.internalSwarm = []
		self.swarmSize  = 0
		self.sortType = Consts.CDefSwarmSortType
		self.sorted = False
		self.minimax = Consts.CDefSwarmMinimax
		
		#Best particle inside topology
		self.bestParticle = None
		
		self.position_updater = FunctionSlot("Position Particles Updater")
		self.information_updater = FunctionSlot("Information Particles Updater")

		self.allSlots = [self.position_updater, self.information_updater]
		
		#Statistics
		self.statted = False
		self.topologyStats = TopologyStatistics()
		self.swarmStats = SwarmStatistics()
				
	def setMinimax(self,minimax):
		""" Sets the swarm minimax
		
		Example:
			>>> swarm.setMinimax(Consts.minimaxType["maximize"])
		
		:param minimax: the minimax type
		
		"""
		self.minimax = minimax
		
	
	def __repr__(self):
		""" Returns the string representation of the topology """
		ret =  "- Topology\n"
		ret += "\nSwarm Size:\t %d\n" % (self.swarmSize,)
		ret += "Sort Type:\t\t %s\n" % (Consts.sortType.keys()[Consts.sortType.values().index(self.sortType)].capitalize(),)
		ret += "\tMinimax Type:\t\t %s\n" % (Consts.minimaxType.keys()[Consts.minimaxType.values().index(self.minimax)].capitalize(),)
		for slot in self.allSlots:
			ret+= "\t" + slot.__repr__()
		ret += "\n"
		ret+= self.topologyStats.__repr__()
		return ret
	
	
	def setTopologyStatistics(self,topStats):
		""" Sets the topology Statistics (Best Particle info)

			Example:
				>>> topology.setTopologyStatistics(FloatStatistics.TopologyStatistics())

			:param topStats: the statistics instance class (must be extend Statistics base class)

		"""
		self.topologyStats = topStats
	
	
	def setSwarmStatistics(self,swarmStats):
		""" Sets the Swarm Statistics (Swarm info)

			Example:
				>>> topology.setSwarmStatistics(FloatStatistics.SwarmStatistics())

			:param swarmStats: the statistics instance class (must be extend Statistics base class)

		"""
		self.swarmStats = swarmStats
	
		
	def __len__(self):
		""" Return the length of the swarm """
		return len(self.internalSwarm)
	
	
	def __getitem__(self, key):
		""" Returns the specified particle from topology """
		return self.internalSwarm[key]
		
	
	def __iter__(self):
		""" Returns the iterator of the swarm """
		return iter(self.internalSwarm)
		
	def __setitem__(self,key,value):
		""" Set the particle of swarm """
		self.internalSwarm[key]  = value
		self.__clear_flags()
		
	def clear_flags(self):
	    self.statted = False
        #self.statted = False
        
	def statistics(self):
		"""Do the statistical analysis of the swarm and set 'statted' to True """
		if self.statted: return
		fit_sum = 0.0
		swarm_size = len(self.internalSwarm)
		for index in xrange(swarm_size):
			fit_sum += self.internalSwarm[index].fitness
		self.swarmStats["fitMax"] = max(self.internalSwarm,key=key_fitness_score).fitness
		self.swarmStats["fitMin"] = min(self.internalSwarm,key=key_fitness_score).fitness
		self.swarmStats["fitAvg"] = fit_sum / float(swarm_size)
        
		bestFit_sum = 0
		for index in xrange(swarm_size):
			bestFit_sum += self.internalSwarm[index].ownBestFitness
		self.swarmStats["bestFitMin"] = min(self.internalSwarm,key=key_best_fitness_score).ownBestFitness
		self.swarmStats["bestFitMax"] = max(self.internalSwarm,key=key_best_fitness_score).ownBestFitness
		self.swarmStats["bestFitAvg"] = bestFit_sum / float(swarm_size)
        
		tmpvar = 0.0
		for index in xrange(swarm_size):
			s = self.internalSwarm[index].ownBestFitness - self.swarmStats["bestFitAvg"]
			s*=s
			tmpvar += s
		tmpvar /= float((len(self.internalSwarm)-1))
		self.swarmStats["bestFitVar"] = tmpvar
		self.swarmStats["bestFitDev"] = math.sqrt(tmpvar)
		self.topologyStats["bestFitness"] = self.bestParticle.ownBestFitness
		self.topologyStats["bestPosition"] = self.bestParticle.ownBestPosition[:]
		self.topologyStats["bestPosDim"] = self.bestParticle.ownBestPosition[0]
		self.topologyStats["position"] = self.bestParticle.position[:]
		self.topologyStats["fitness"] = self.bestParticle.fitness
        
		self.statted = True	
		
	def getBestParticle(self):
		""" Return the best particle of the swarm
		:rtype: the particle
		
		"""
		return self.bestParticle


	def sort(self):
		""" Sort the swarm """
		if self.sorted: return
		rev = (self.minimax == Consts.minimaxType["maximize"])
		
		if self.sortType == Consts.sortType["fitness"]:
			self.internalSwarm.sort(cmp=cmp_particle_fitness, reverse=rev)

		self.sorted = True
		
		
	
	def setSwarmSize(self, size):
		""" Set the population size
			:param size: the population size
		"""
		self.swarmSize = size

	
	def setSortType(self,sort_type):
		""" Sets the sort type
			Example:
				>>> swarm.setSortType(Consts.sortType["scaled"])
			
		:param sort_type: the Sort Type

		"""
		self.sortType = sort_type
	
	
	def setBestParticle(self,particle):
		""" Set the best Particle
			Example:
				>>> topology.setBestParticle(bestParticle)
		
		:param particle: the best particle to set
		"""
		self.bestParticle = particle


	def create(self, **args):
		""" Clone the example particle fo fill the swarm """
		self.clear()
		self.minimax  = args["minimax"]
		for i in xrange(self.swarmSize):
			self.internalSwarm.append(self.oneSelfParticle.clone())
		self.clear_flags()
	
	def initialize(self):
		""" Initialize all particles of swarm 
		this calls the initialize() of particles
		
		PS: You can OVERRIDE this method for custom initialization.
		 """
		for particle in self.internalSwarm:
			particle.initializePosition()
			particle.initializeVelocity()
			particle.evaluate()
			particle.ownBestFitness = particle.fitness
			
		self.bestParticle = self.internalSwarm[0]
		self.clear_flags()
	
	
	def evaluate(self,*args):
		""" Evaluate all particles in swarm, calls the evaluate() method of particles
		
		:param args: this param are passed to the evaluation function
		
		"""
		for particle in self.internalSwarm:
			particle.evaluate(**args)
		self.clear_flags()
		


	def printStats(self):
		""" Print statistics of the current population """
		message = ""
		#message = "[Swarm] - Max/Min/Avg bestFitness(Fitness) [%.2f(%.2f)/%.2f(%.2f)/%.2f(%.2f)]\n" %  (self.stats["bestFitMax"], self.stats["fitMax"], self.stats["fitMin"], self.stats["bestFitMin"], self.stats["bestFitAvg"], self.stats["fitAvg"])      
		message+= "[Topology] - bestFitness/bestPosDim  [%s/%s]" % (self.topologyStats["bestFitness"], self.topologyStats["bestPosDim"])
		print message
		return message

	def clear(self):
		""" Remove all particles from swarm """
		del self.internalSwarm[:]
		self.clear_flags()

		
	def getStatistics(self):
		""" Return a Statistics classes for statistics
        
        :rtype: the  subclasses of :class: `Statistics.Statistics`  (topology,swarm) instances 
        
		"""
		self.statistics()	
		self.clear_flags()
		return (self.topologyStats, self.swarmStats)     
    