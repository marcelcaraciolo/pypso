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
'''

'''
    This module contains the class Topology, which is responsable to stablish
    the information change between particles.
'''

from pypso import SwarmStatistics
from pypso import TopologyStatistics
from pypso import Particle
import math

#A key function to return the fitness score, used by max()/min()
#@param particle: the particle instance
#@return the particle fitness
def key_fitness(particle):
    return particle.fitness

#A Key function to return the best fitness score from the particle, used by max()/min()
#@param particle: the particle instance
#@return the particle best fitness
def key_bestFitness(particle):
    return particle.ownBestFitness


##Class Topology - The container for the particles
class Topology(object):
    
    #Communicator used by the particles in this topology. 
    #You can change the default communicator using the *set* function
    communicator = None
    
    
    #The topology class constructor
    def __init__(self):
        #Number of particles inside swarm 
        self.swarmSize = 0
        #Number of search space dimensions
        self.dimensions = 0
        #Swarm used by the topology
        self.swarm = []
        #Best particle inside topology
        self.bestParticle = None
        # Statistics Flag
        self.statted = False
        #Swarm Statistics (all particles)
        self.swarmStats   =  SwarmStatistics.SwarmStatistics()
        #The best particle of topology statistics
        self.topologyStats = TopologyStatistics.TopologyStatistics()
        
        
    #Initialize the topology
    def initialize(self):
        self.createSwarm()
        self.initializeSwarm()
    
    #Creates the swarm
    def createSwarm(self):
        self.clear()
        for i in xrange(self.swarmSize):
            self.swarm.append(Particle.Particle())
        
        
    #Initializes the particles of the swarm
    def initializeSwarm(self):
        for particle in self.swarm:
            particle.initialize(self.dimensions)
            
        self.bestParticle = self.swarm[0]
    
    #Updates the topology information
    def updateParticlesInformation(self):
        pass
    
    #Updates the topology particles position
    def updateParticlesPosition(self):
        pass
    
    #Remove all particles from swarm
    def clear(self):
        del self.swarm[:]
    
    #Gets the best Particle found so far.
    #@return bestParticle: The best particle found.
    def getBestParticle(self):
        return self.bestParticle
    
    #@return returns the swarm
    def getSwarm(self):
        return self.swarm
    
    #@param dimensions The dimensions to set
    def setDimensions(self,dimensions):
        if dimensions < 1:
            Util.raiseException("Number of dimensions must be >=1",ValueError)
        self.dimensions = dimensions
  
    #Set the swarm size
    #@param size: the swarm size 
    def setSwarmSize(self,size):
        if size < 2:
            Util.raiseException("Swarm size must be >= 2", ValueError)
        self.swarmSize = size

    
    #Set the best Particle
    #@param particle: The best particle to set
    def setBestParticle(self,particle):
        self.bestParticle = particle
    
    
    #Returns the string representation of the topology
    def __repr__(self):
        ret = "- Topology\n"
        ret += "\tSwarm Size:\t %d\n" %(self.swarmSize,)
        ret += "\tDimensions:\t %d\n" %(self.dimensions,)
        ret += "\tCommunicator:\t\t %s\n" %(self.communicator)
        ret += "\n"
        return ret
    
    #Do the statistical analysis of the swarm and set 'statted' to True
    def statistics(self):
        if self.statted: return
        fit_sum = 0.0
        swarm_size = len(self.swarm)
        for index in xrange(swarm_size):
            fit_sum += self.swarm[index].fitness
        self.swarmStats["fitMax"] = max(self.swarm,key=key_fitness).fitness
        self.swarmStats["fitMin"] = min(self.swarm,key=key_fitness).fitness
        self.swarmStats["fitAvg"] = fit_sum / float(swarm_size)
        
        bestFit_sum = 0
        for index in xrange(swarm_size):
            bestFit_sum += self.swarm[index].ownBestFitness
        self.swarmStats["bestFitMin"] = min(self.swarm,key=key_bestFitness).ownBestFitness
        self.swarmStats["bestFitMax"] = max(self.swarm,key=key_bestFitness).ownBestFitness
        self.swarmStats["bestFitAvg"] = bestFit_sum / float(swarm_size)
        
        tmpvar = 0.0
        for index in xrange(swarm_size):
            s = self.swarm[index].ownBestFitness - self.swarmStats["bestFitAvg"]
            s*=s
            tmpvar += s
        tmpvar /= float((len(self.swarm)-1))
        self.swarmStats["bestFitVar"] = tmpvar
        self.swarmStats["bestFitDev"] = math.sqrt(tmpvar)
        
        self.topologyStats["bestFitness"] = self.bestParticle.ownBestFitness
        self.topologyStats["bestPosition"] = self.bestParticle.ownBestPosition[:]
        self.topologyStats["bestPosDim"] = self.bestParticle.ownBestPosition[0]
        self.topologyStats["position"] = self.bestParticle.position[:]
        
        
        self.statted = True
    
    #Print statistics of the swarm
    def printStats(self):
        message = ""
        #message = "[Swarm] - Max/Min/Avg bestFitness(Fitness) [%.2f(%.2f)/%.2f(%.2f)/%.2f(%.2f)]\n" %  (self.stats["bestFitMax"], self.stats["fitMax"], self.stats["fitMin"], self.stats["bestFitMin"], self.stats["bestFitAvg"], self.stats["fitAvg"])      
        message+= "[Topology] - bestFitness/bestPosDim  [%s/%s]" % (self.topologyStats["bestFitness"], self.topologyStats["bestPosDim"])
        print message
        return message
    
    #Clear all stats flags
    def clearFlags(self):
        self.statted = False
    
  
        
        

