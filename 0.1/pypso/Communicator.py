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
    This module contains the class Particle communicator class, which is responsable to 
    realize how the information and position of the particle is updated.
'''

#Particle communicator interface
class Communicator(object):
    
    #Update the particle position inside the search space
    #@param particle: the particle to be updated
    #@param topology: The topology of the particle
    #@param c1 : cognitive coefficient acceleration
    #@param c2 : social   coefficient acceleration
    def updateParticlePosition(self,particle,topology,c1,c2):
        pass
    
    #Update the particle information (fitness)
    #@param particle: The particle to be updated
    #@param topology: The topology of the particle
    def updateParticleInformation(self,particle,topology):
        pass
