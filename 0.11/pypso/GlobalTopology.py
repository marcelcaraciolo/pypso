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

0.10 2009-04-18 Initial version.
0.23 2009-09-10 Added support for new API and Docs.
'''

"""
:mod:`GlobalTopology` -- the Global Topology
================================================================

    This is the Global Topology representation.
    This topology class extends the :class:`TopologyBase.TopologyBase` class.

"""

from TopologyBase import *

def updateParticlesInformation(pso_engine, **args):
	""" Update Particle Information function of Global Topology
	
	"""
	for particle in pso_engine.topology.internalSwarm:
		args["pso_engine"] = pso_engine
		for it in particle.information_communicator.applyFunctions(particle,**args):
			pass
	pso_engine.topology.clear_flags()


def updateParticlesPosition(pso_engine, **args):
	""" Update Particle Position function of Global Topology
	"""
	for particle in pso_engine.topology.internalSwarm:
		args["pso_engine"] = pso_engine
		for it in particle.position_communicator.applyFunctions(particle,**args):
			pass
		particle.evaluate()

class GlobalTopology(TopologyBase):
	
	""" GLobal Topology Class - The container for the swarm

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
		""" The Star Topology Class Creator , particle representation must be specified."""
		TopologyBase.__init__(self,particle)
		
		self.position_updater.set(updateParticlesPosition)
		self.information_updater.set(updateParticlesInformation)
		

	
	def __repr__(self):
		""""Return a string representation of the Glboal Topology """
		ret = TopologyBase.__repr__(self)
		ret += "-Global Topology\n"
		return ret
		
    
    
    
