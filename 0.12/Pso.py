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
0.20 2009-05-21 Added support for Local Topology implementation (Added StoreBestParticle method).
0.21 2009-05-24 Added support for Linux interaction.
0.22 2009-05-25 Added support for report files generation (Uses ReportAdapters).
0.22 2009-06-08 Fixed some bugs related to the INERTIA factor.
0.23 2009-09-09 Redesigned all the class for support new API and Docs.
'''

"""    

:mod:`SimplePSO` -- the pso algorithm by itself
====================================================================
This module contains the PSO Engine, the PSO class is responsible
for all the evolutionary process. It contains the PSO Algorithm related
functions, like the Termination Criteria functions for convergence analysis, and
the topology base class used to do the particle communication.

"""
import random
import Consts
import code
from time import time
from FunctionSlot import FunctionSlot
from sys import platform as sys_platform


if sys_platform[:3] == "win":
   import msvcrt
elif sys_platform[:5] == "linux":
    import atexit
    atexit.register(Util.set_normal_term)
    Util.set_curses_term()


def FitnessScoreCriteria(pso_engine):
	""" Terminate the evolution using the bestFitness parameter obtained from the particle

	Example:
		>>> particleRep.setParams(bestFitness=0.00, roundDecimal=2)
		(...)
		>>> pso_engine.terminationCriteria.set(Pso.FitnessScoreCriteria)

	"""
	particle = pso_engine.bestParticle()
	bestFitness = particle.getParam("bestFitness")
	roundDecimal = particle.getParam("roundDecimal")
	
	if bestFitness is None:
		Util.raiseException("You must specify the bestFitness parameter", ValueError)
	
	if pso_engine.getMinimax() == Consts.minimaxType["maximize"]:
		if roundDecimal is not None:
			return round(bestFitness,roundDecimal) <= round(particle.ownBestFitness,roundDecimal)
		else:
			return bestFitness < particle.ownBestFitness
	
	else:
		if roundDecimal is not None:
			return round(bestFitness,roundDecimal) >= round(particle.ownBestFitness, roundDecimal)
		else:
			return bestFitness >= particle.ownBestFitness
	
	return flag




class SimplePSO(object):
	""" SimplePSO Engine Class - The PSO Algorithm Core
	
	Example:
		>>> topology = Topology.GlobalTopology(particle_rep)
		>>> pso = PSO.SimplePSO(topology)
		>>> pso.setSteps(120)
	
	:param topology: the :term:`Sample Topology``
	:param  interactiveMode: this flag enables the Interactive Mode
	:param seed: the random seed value
	
	.. note:: if you see the same random seed, all the runs of the algorithm will be the same.
	
	"""
	
	stepCallBack = None
	""" This is the the :term: `step callback function` slot,
	if you want to set the function, you must do this: ::
		
		def your_func(pso_engine):
			#Here you have access to the PSO Engine
			return False
		
		pso_engine.stepCallback.set(your_func)
	
	now *"your_func"* will be called every step.
	When this function returns True, the  PSO Engine will stop the evolution and show
	a warning, if is False, the evolution continues.
	"""
	
	terminationCriteria  = None
	""" This is the termination criteria slot, if you want to set one 
	termination criteria, you mus do this: ::
		
		pso_engine.terminationCriteria.set(your_func)
		
	Now, when you run your PSO, it will stop when terminationCriteria be satisfied.
	
	To create your own termination function, you must put at least one parameter
	which is the PSO Engine, follows an example: ::
		
		def ConvergenceCriteria(pso_engine):
			swarm = pso_engine.getSwarm()
			return swarm[0] == swarm[len(swarm)-1]
		
	When this function returns True, the Pso Engine will stop the evolution and show
	a warning. If is False, the evolution  continues, this function is called every
	step.
	
	"""
	
	def __init__(self,topology,seed=None,interactiveMode=True):
		""" Initializator of PSO """
		#random seed
		random.seed(seed)
		#Pso type used by the particle
		self.psoType = Consts.CDefPsoType
		#Topology used
		self.topology = topology
		#Set the population size
		self.setSwarmSize(Consts.CDefSwarmSize)
		#Cognitive and Social Coefficients
		self.C1,self.C2 = Consts.CDefCoefficients
        #Time steps
		self.timeSteps = Consts.CDefSteps
		#Interactive Mode (True or False)
		self.interactiveMode = interactiveMode
		#Current step
		self.currentStep = 0
		#Inertia Factor Minus
		self.inertiaFactorMinus = None
		#Inertia coefficient
		self.inertiaFactor = None
		#Time initial
		self.time_init = None
	    #Optimization type
		self.minimax = Consts.minimaxType["minimize"]
		#Report file adapter 
		self.reportAdapter = None
		#Step Callback
		self.stepCallback = FunctionSlot("Step Callback")
		#Termination Criteria
		self.terminationCriteria = FunctionSlot("Termination Criteria")
		#All slots
		self.allSlots = [self.stepCallback, self.terminationCriteria]
		
		print "A PSO Engine was created, timeSteps=% d" % ( self.timeSteps, )


	def __repr__(self):
		""" The String representation of the PSO Engine """
		ret =   "- PSO-%s-%s Execution\n" % (self.getTopologyType(),self.getPsoType())
		ret +=  "\tSwarm Size:\t %d\n" % (self.topology.swarmSize,)
		ret +=  "\tTime Steps:\t %d\n" % (self.timeSteps,)      
		ret +=  "\tCurrent Step:\t %d\n" % (self.currentStep,)
		ret +=  "\tMinimax Type:\t %s\n" % (Consts.minimaxType.keys()[Consts.minimaxType.values().index(self.minimax)].capitalize(),)
		ret +=  "\tReport Adapter:\t %s\n" % (self.reportAdapter,)
		for slot in self.allSlots:
			ret += "\t" + slot.__repr__()
		ret +="\n"
		return ret

	def setReportAdapter(self,repadapter):
		""" Sets the Report Adapter of the PSO Engine
		
		:param repadapter: one of the :mod:`ReportAdapters` classes instance
		
		.. warning: the use of a Report Adapter can reduce the speed performance of the PSO.
		
		"""
		self.reportAdapter = repadapter
		
	
	def setSwarmSize(self, size):
		""" Sets the swarm size, calls setSwarmSize()  of Topology
		
		:param size: the swarm size
		
		.. note:: the swarm size must be >= 2
		
		"""
		if size < 2:
			Util.raiseException("swarm size must be >= 2", ValueError)
		self.topology.setSwarmSize(size)
	


	def setPsoType(self,psoType):
		""" Sets the psoType, use Consts.psoType(Basic,Constricted,Inertia)
		
		Example:
			>>> pso_engine.setSortType(Consts.psoType["CONSTRICTED"])
      
        :param psoType: The PSO type, from Consts.psoType
        
		"""
		if psoType not in Consts.psoType.values():
			Util.raiseException("PsoType must be implemented !",TypeError)
		self.psoType = psoType

	def getPsoType(self):
		""" Return the Pso Type
		
		:rtype key: pso Type
		"""	
		for key,value in Consts.psoType.items():
			if value == self.psoType:
				return key
		return ""

	def setTimeSteps(self,num_steps):
		""" Sets the number of steps to converge
		
		:param num_steps: the number of steps
		
		"""
		if num_steps < 1:
			Util.raiseException("Number of steps must be >=1", ValueError)
		self.timeSteps = num_steps


	def getMinimax(self):
		""" Gets the minimize/maximize mode
		
		:rtype: The Consts.minimaxType type
		
		"""
		for key,value in Consts.minimaxType.items():
			if value == self.minimax:
				return key
			return ""
			

	
	def getTopologyType(self):
		""" Returns the name of the topology
		
		:rtype name: the name of the topology
		 """
		return self.topology.__class__.__name__

	def setMinimax(self,minimax):
		"""Sets the minimize/maximize mode, use Consts.minimaxType
		
		:param minimax: the minimax mode, from Consts.minimaxType
		
		"""
		if minimax not in Consts.minimaxType.values():
			Util.raiseException("Optimization type must be Maximize or Minimize !", TypeError)
		
		self.minimax = minimax	

	def getCurrentStep(self):
		""" Gets the current step
		
		:rtype: the current step
		"""
		return self.currentStep

	def getReportAdapter(self):
		""" Gets the Report Adapter of the PSO Engine
		
		:rtype: a instance from one of the :mod:`ReportAdapters` classes
		
		"""
		return self.reportAdapter
	
	
	def bestParticle(self):
		""" Returns the swarm best Particle
		
		:rtype: the best particle
		
		"""
		return self.topology.getBestParticle()
		
	def getTopology(self):
		"""Return the internal topology of Pso Engine
		
		:rtype: the topology (:class: 'Topology.Topology')'
	
		"""
		return self.topology
		

	def getStatistics(self):
		""" Gets the Statistics class instance of the current step
		
		:rtype: the statistics instance (:class: `Statistics.Statistics`)`
		
		"""
		return self.topology.getStatistics()

	def dumpStatsReport(self):
		""" Dumps the current statistics to the  report adapter """
		self.topology.statistics()
		self.reportAdapter.insert(self.getStatistics(),self.topology,self.currentStep)
		
		
	def printStats(self):
		""" Print swarm statistics"""
		percent = self.currentStep * 100 / float(self.timeSteps)
		message = "Step: %d (%.2f%%):" % (self.currentStep, percent)
		print message
		self.topology.statistics()
		self.topology.printStats()

	
	def printTimeElapsed(self):
		""" Shows the time elapsed since the beginning of the solution construction """
		print "Total time elapsed: %.3f seconds." % (time()-self.time_init)
    	
	
	def initialize(self):
		""" Initializes the PSO Engine. Create and initialize the swarm """
		self.topology.create(minimax=self.minimax)
		self.topology.initialize()
		print "The PSO Engine was initialized !"
	
	
	def constructSolution(self):
		""" Just do one step in execution, one step."""
		for it in self.topology.position_updater.applyFunctions(self):
			pass

		for it in self.topology.information_updater.applyFunctions(self):
			pass
		
		if self.psoType == Consts.psoType["INERTIA"]:
			self.updateInertiaFactor()
		
		self.currentStep += 1
		
		return (self.currentStep == self.timeSteps)


	
	def execute(self, freq_stats=0):
		""" Do all the steps until the termination criteria or time Steps achieved,
		accepts the freq_stats (default is 0) to dump statistics at n-step
		
		Example:
			>>> pso_engine.evolve(freq_stats=10)
			(...)
		
		:param freq_stats: if greater than 0, the statistics will be 
							printed every freq_stats step.

		"""
		#Start time
		self.time_init = time()
		
		#Creates a new report if reportAdapter is not None.
		if  self.reportAdapter: self.reportAdapter.open()
		
		#Initialize the PSO Engine
		self.initialize()  #Already evaluates all particles


		print "Starting loop over evolutionary algorithm."
		
		try:
			while not self.constructSolution():
				stopFlagCallback = False
				stopFlagTerminationCriteria = False
				
				if not self.stepCallback.isEmpty():
					for it in self.stepCallback.applyFunctions(self):
						stopFlagCallback = it
					
				if not self.terminationCriteria.isEmpty():
					for it in self.terminationCriteria.applyFunctions(self):
						stopFlagTerminationCriteria = it
				
				if freq_stats != 0:
					if (self.currentStep % freq_stats == 0) or (self.currentStep == 1):
						self.printStats()
					
				if self.reportAdapter:
					if self.currentStep % self.reportAdapter.statsGenFreq == 0:
						self.dumpStatsReport()
				
				if stopFlagTerminationCriteria:
					print '\n\tExecution stopped by Termination Criteria function !\n'
					break
				
				if stopFlagCallback:
					print '\n\tExecution stopped by Step Callback function!\n'
					break

			  
				if self.interactiveMode:
					if sys_platform[:3] == "win":
						if msvcrt.kbhit():
							if ord(msvcrt.getch()) == Consts.CDefESCKey:
								print "Loading modules for Interactive mode...",
								import pypso.Interaction
								print "done!\n"
								interact_banner = "## PyPSO v.%s - Interactive Mode ##\nPress CTRL-Z to quit interactive mode." % (pypso.__version__,)
								session_locals = {  "pso_engine"  : self,
													"topology" : self.getTopology(),
													"swarm_statistics": self.getTopology().swarmStats,
													"topology_statistics": self.getTopology().topologyStats,
													"pypso"   : pypso ,
													"it"         : pypso.Interaction}
								print
								code.interact(interact_banner, local=session_locals)
					elif sys_platform[:5] == "linux":
						if Util.kbhit():
							if ord(Util.getch()) == Consts.CDefESCKey:
								print "Loading modules for Interactive mode...",
								import pypso.Interaction
								print "done!\n"
								interact_banner = "## PyPSO v.%s - Interactive Mode ##\nPress CTRL-D to quit interactive mode." % (pypso.__version__,)
								session_locals = {  "pso_engine"  : self,
													"topology" : self.getTopology(),
													"swarm_statistics": self.getTopology().swarmStats,
													"topology_statistics": self.getTopology().topologyStats,
													"pypso"   : pypso ,
													"it"         : pypso.Interaction}
								print
								code.interact(interact_banner, local=session_locals)
                                    
		except KeyboardInterrupt:
			print "\n\tA break was detected, you have interrupted the evolution !\n"

		if freq_stats != 0:
			self.printStats()
			self.printTimeElapsed()
    
		if self.reportAdapter:
			if (self.currentStep % self.reportAdapter.statsGenFreq == 0):
				self.dumpStatsReport()
			self.reportAdapter.saveAndClose()	
		
		
		