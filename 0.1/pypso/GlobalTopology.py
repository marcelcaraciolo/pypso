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
'''

'''
    This module contains the class Global Topology, which extends
    the basic topology class.
'''


from pypso import Topology
from pypso import GlobalComunicator
from pypso import Pso


##Class Global Topology - The Star Topology
class GlobalTopology(Topology.Topology):
    
    #Class Constructor
    #@param swarmSize : The number of particles used by the topology.
    #@param dimensions: The numbero of dimensions used by the particles.
    def __init__(self,swarmSize,dimensions):
        #Call the superclass constructor
        super(GlobalTopology,self).__init__()
        #Number of particles inside swarm 
        self.setSwarmSize(swarmSize)
        #Number of search space dimensions
        self.setDimensions(dimensions)
        #The communicator used by the topology.
        self.communicator = GlobalComunicator.GlobalCommunicator()

    #Initialize the swarm
    def initialize(self):
        super(GlobalTopology,self).initialize()
        #Updates the particle information
        self.updateParticlesInformation()
    
    #Updates the particles information
    def updateParticlesInformation(self):
        for particle in self.swarm:
            particle.setCommunicator(self.communicator)
            particle.getCommunicator().updateParticleInformation(particle,self)
        self.clearFlags()
    
    #Updates the particles position
    def updateParticlesPosition(self):
        for particle in self.swarm:
            particle.getCommunicator().updateParticlePosition(particle,self,Pso.PSO().C1,Pso.PSO().C2)
            particle.evaluateFitness()
    
    
    
    
    
