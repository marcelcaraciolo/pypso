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
    This module contains the class GlobalCommunicator used by global topology, 
    which extends the basic  is responsable to realize how the information and position of the 
    particle is updated.
'''

from pypso import Communicator
from pypso import Pso
from pypso import Consts
import random
from pypso import Util
import math
##Communicator used by Global topology
class GlobalCommunicator(Communicator.Communicator):    

    #@OVERRIDE
    def updateParticlePosition(self,particle,topology,c1,c2):
        rand = random.Random()
        
        for i in xrange(len(particle.getPosition())):
            
            #Update velocity 
            if Pso.PSO().psoType == Consts.psoType["BASIC"]:
                particle.getVelocity()[i] = particle.getVelocity()[i] + c1 * rand.random() * (particle.getownBestPosition()[i] - particle.getPosition()[i]) + \
                                             c2 * rand.random() * (topology.getBestParticle().getownBestPosition()[i] - particle.getPosition()[i])
            elif Pso.PSO().psoType == Consts.psoType["INERTIA"]:
                print 'not yet implemented'
                #particle.getVelocity()[i] = PsoImpl.getInstance().getInertiaFactor() * particle.getVelocity()[i] + c1 * random1.nextDouble() * (particle.getPPosition()[i] - particle.getPosition()[i]) + c2
                #        * random2.nextDouble() * (topology.getPGParticle().getPPosition()[i] - particle.getPosition()[i]);
            elif Pso.PSO().psoType == Consts.psoType["CONSTRICTED"]:
                fi = c1 + c2
                k = 2.0 / abs(2.0 - fi - math.sqrt(math.pow(fi,2) - 4 * fi))
                particle.getVelocity()[i] = k * (particle.getVelocity()[i] + c1 * rand.random() * (particle.getownBestPosition()[i] - particle.getPosition()[i]) + \
                                                 c2 * rand.random() * (topology.getBestParticle().getownBestPosition()[i] - particle.getPosition()[i]))                                                
            else:
                Util.raiseException("PsoType not yet implemented.",TypeError)
            
            #Velocity limit
            if particle.getVelocity()[i] > Pso.PSO().velocityBounds[i]:
                particle.getVelocity()[i] = Pso.PSO().velocityBounds[i]
            elif particle.getVelocity()[i] < (Pso.PSO().velocityBounds[i] * (-1)):
                particle.getVelocity()[i] = Pso.PSO().velocityBounds[i] * (-1)
                
            #Update position
            particle.getPosition()[i] = particle.getPosition()[i] + particle.getVelocity()[i]
            
            #Search space limit
            if particle.getPosition()[i] > Pso.PSO().positionBounds[i][1]:
                particle.getPosition()[i] = Pso.PSO().positionBounds[i][1]
                particle.getVelocity()[i] = particle.getVelocity()[i] * (-1)
            elif particle.getPosition()[i] < Pso.PSO().positionBounds[i][0]:
                particle.getPosition()[i] = Pso.PSO().positionBounds[i][0]
                particle.getVelocity()[i] = particle.getVelocity()[i] * (-1)
    
    
    
    
    #@OVERRIDE
    def updateParticleInformation(self,particle,topology):
        if Pso.PSO().minimax == Consts.minimaxType["maximize"]:
            #update globalParticle information
            if (particle.getFitness() > particle.getownBestFitness()):
                particle.setownBestFitness(particle.getFitness())
                particle.setownBestPosition(particle.getPosition())
            #update topology swarm information
            if particle.getownBestFitness() > topology.getBestParticle().getownBestFitness():
                topology.setBestParticle(particle)
            
        else:
            #update global Particle information
            if (particle.getFitness() < particle.getownBestFitness()):
                particle.setownBestFitness(particle.getFitness())
                particle.setownBestPosition(particle.getPosition())
            #update topology swarm information
            if particle.getownBestFitness() < topology.getBestParticle().getownBestFitness():
                topology.setBestParticle(particle)
            
        
    
    

