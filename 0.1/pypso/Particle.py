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
    This module have the class which every particle of the swarm extends,
    If you are planning to create a new representation, you must take a
    inside look into this module.
'''
import random
from pypso import Pso

##Particle Class - The base of all particle representation
class Particle(object):
    
    #Communicator used by the particle. You can change the default
    #communicator using the *set* function
    communicator = None

    #Class Constructor
    def __init__(self):
        
        #Current velocity.
        self.velocity = []
        #Current position.
        self.position = []
        #Best fitness founded by particle
        self.ownBestFitness = 0.0
        #Best position founded by particle.
        self.ownBestPosition = []
        #Current fitness
        self.fitness = 0.0
    
    
    #Initialize the particles.
    #@param dimensions: Number of dimensions used.
    def initialize(self,dimensions):
        for i in xrange(dimensions):
            #Fill positions from low up to high position bound.
            rand = self.randomPosition(Pso.PSO().initialPositionBounds[i][0],Pso.PSO().initialPositionBounds[i][1])
            self.position.append(rand)
            self.ownBestPosition.append(rand)
            #Velocities from 0.0 up to velocity bound
            rand = abs(random.uniform(0.0,Pso.PSO().velocityBounds[i]))
            self.velocity.append(rand)
        #Calculate the fitness
        self.evaluateFitness()
        self.ownBestFitness = self.fitness
    
    
    #Evaluates the particle fitness
    def evaluateFitness(self):   
        self.fitness = Pso.PSO().function(self.position)
    #Get an random Position
    #@param min: The min value
    #@param max: The max value
    def randomPosition(self,min,max):
        return min + (max - min) * (random.random())
    
    #Get the fitness score of the particle
    #@return fitness
    def getFitness(self):
        return self.fitness
    
    #Get the particle communicator
    #@return communicator
    def getCommunicator(self):
        return self.communicator
    
    #Get the current Position
    #@return current Position
    def getPosition(self):
        return self.position
    
    #Get the current velocity
    #@return current velocity
    def getVelocity(self):
        return self.velocity
    
    #Get the own best Fitness
    #@return the own best Fitness
    def getownBestFitness(self):
        return self.ownBestFitness
  
    #Get the best position founded by particle.
    def getownBestPosition(self):
        return self.ownBestPosition
    
    #Set the particle communicator
    #@param communicator: The particle communicator
    def setCommunicator(self,communicator):
        self.communicator = communicator
    
    #Set the own best fitness
    #@param ownBestFitness : The best fitness
    def setownBestFitness(self,ownBestFitness):
        self.ownBestFitness = ownBestFitness
        
    #Set the own best position
    #@param ownBestPosition : The best position
    def setownBestPosition(self,ownBestPosition):
        self.ownBestPosition = ownBestPosition[:]     
    
    #Clear best position and fitness of the particle
    def resetStats(self):
        self.ownBestFitness = 0.0
        self.fitness = 0.0
        self.ownBestPosition = []
    
    #String represenation of the Particle
    def __repr__(self):
        ret = "-Particle\n"
        ret+= "\tFitness:\t\t\t %s\n" %(self.fitness,)
        ret+= "\tBestFitness:\t\t\t %s\n" % (self.ownBestFitness,)
        ret+= "\tBestPosition:\t\t %s\n\n" % (self.ownBestPosition,)
        return ret
        
        

