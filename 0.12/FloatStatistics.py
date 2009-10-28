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
0.23 2009-09-15 Added the class Swarm Statistics and changed the name to Float Statistics. New API and redesign.
'''

"""
:mod:`FloatStatistics` -- the  Real Representation (Float numbers) statistics.
================================================================

	This module have the Topology Statistics and Swarm Statistics Class. 
	The Topology Statistics Class is responsable to keep
	the information about the best particle of the topology at each timeStep
	during the evolution proccess. 
	The Swarm Statistics is responsible to keep the statistics of the PSO Swarm.
	Those Statistics classes extends the :class:`Statistics.Statistics` class.

"""

import Statistics

class TopologyStatistics(Statistics.Statistics):
	""" Topology Statistics Class - A class bean-like to store the statistics

	The statistics hold by this class are:

	**bestFitness, fitness**
      Best and current fitness scores of the best particle

	**position, bestPosition**
      current position and the best position of the best particle

	**bestPosDim**
      Best First Dimmension Position of the best Particle

	Example:
		>>> stats = topologyStatistics.getStatistics()
		>>> stats["fitness"]
		10.2
   """

	def __init__(self):
		""" The Topology Statistics Class Creator """
		#Call the superclass constructor
		super(TopologyStatistics,self).__init__()
		#'fit means  'fitness'
		self.internalDict = {   "bestFitness"   : 0.0,
                                "fitness"       : 0.0,
                                "bestPosition"  : [],
                                "bestPosDim:"   : 0.0,
                                "position"      : []
                             }
   
		self.descriptions = {   "bestFitness"  : "Best Fitness of the best Particle",
                                "fitness"      : "Fitness of the best Particle",
                                "bestPosition" : "Best Position of the best Particle",
                                "bestPosDim:"  : "Best 1st Dim. Position of the best Particle",
                                "position"     : "Position of the best Particle"
                            } 

	def __repr__(self):
		""" Return a string representation of the statistics """
		strBuff = "- Best Particle Topology Statistics\n"
		for k,v in self.internalDict.items():
			strBuff += "\t%-45s = %s\n" % (self.descriptions.get(k,k), v)
		return strBuff




class SwarmStatistics(Statistics.Statistics):
	""" Swarm Statistics Class - A class bean-like to store the statistics

	The statistics hold by this class are:

	**bestFitMax, bestFitMin**
      The maximum and minimum fitness scores of the swarm

	**bestFitAvg,bestFitDev**
      The Average and Standard Deviation of the best fitness of the swarm

	**fitMin, fitMax, fitAvg**
     	Minimum fitness, Maximum fitness and Fitness Average of the swarm

	Example:
		>>> stats = topology.getStatistics()
		>>> stats["fitMin"]
		10.2
	"""

	def __init__(self):
		""" The Statistics Class Creator """
		#Call the superclass constructor
		super(SwarmStatistics,self).__init__()
		#'fit means  'fitness'
		self.internalDict = {   "bestFitMax" : 0.0,
                                "bestFitMin" : 0.0,
                                "bestFitAvg" : 0.0,
                                "bestFitDev" : 0.0,
                                "bestFitVar" : 0.0,
                                "fitMin"     : 0.0,
                                "fitMax"     : 0.0,
                                "fitAvg"     : 0.0
                             }

		self.descriptions = {   "bestFitMax" : "Maximum best Fitness",
                                "bestFitMin" : "Minimum best Fitness",
                                "bestFitAvg" : "Average of best Fitness",
                                "bestFitDev" : "Standard deviation of best Fitness",
                                "bestFitVar" : "Best Fitness variance",
                                "fitMin" : "Minimum fitness",
                                "fitMax" : "Maximum fitness",
                                "fitAvg" : "Fitness average" 
                            } 

        #Return a string representation of the statistics
	def __repr__(self):
		""" Returns a string representation of the statistics"""
		strBuff = "-Statistics\n"
		for k,v in self.internalDict.items():
			strBuff += "\t%-45s = %.2f\n" % (self.descriptions.get(k,k), v)
		return strBuff


