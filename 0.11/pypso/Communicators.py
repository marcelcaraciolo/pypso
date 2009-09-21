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
0.23 2009-09-10 Changed API, DOCS and name of the class. Reason: Be more generic.
'''

"""

:mod:`Communicators` -- selection methods module
==============================================================

    This module contains the  *Particle communicator* method, which is responsable to 
    realize how the information and position of the particle is updated.

"""

import Util
import Consts
import random
import math

def P1DGlobalPosCommunicator(particle,**args):
	""" Global Communicator - Update method for particle position inside the search space
	
		:param particle: the particle to be updated
	"""
	try:
		pso_engine = args["pso_engine"]
		topology = pso_engine.topology
	except:
		Util.raiseException("to use the P1DGlobalPosCommunicator, you must specify the args['pso_engine'] parameter")
	
	
	rand = random.Random()
	

	for i in xrange(len(particle.getPosition())):
		
		#Update velocity
		if pso_engine.psoType == Consts.psoType["BASIC"]:
			particle.getVelocity()[i] = particle.getVelocity()[i] + pso_engine.C1 * rand.random() * (particle.getOwnBestPosition()[i] - particle.getPosition()[i]) + \
										pso_engine.C2 * rand.random() * (topology.getBestParticle().getOwnBestPosition()[i] - particle.getPosition()[i])
		elif pso_engine.psoType == Consts.psoType["INERTIA"]:

			particle.getVelocity()[i] = Pso.PSO().getInertiaFactor() * particle.getVelocity()[i] + pso_engine.C1 * rand.random() * (particle.getOwnBestPosition()[i] - particle.getPosition()[i]) + \
										pso_engine.C2* rand.random() * (topology.getBestParticle().getOwnBestPosition()[i] - particle.getPosition()[i])
		elif pso_engine.psoType == Consts.psoType["CONSTRICTED"]:
			fi = pso_engine.C1 + pso_engine.C2

			k = 2.0 / abs(2.0 - fi - math.sqrt(math.pow(fi,2) - 4 * fi))

			particle.getVelocity()[i] = k * (particle.getVelocity()[i] + pso_engine.C1 * rand.random() * (particle.getOwnBestPosition()[i] - particle.getPosition()[i]) + \
										pso_engine.C2 * rand.random() * (topology.getBestParticle().getOwnBestPosition()[i] - particle.getPosition()[i]))    
			
                                           
		else:
			Util.raiseException("PsoType not yet implemented.",TypeError)
            
		#Velocity limit
 		if particle.getVelocity()[i] > particle.getParam("rangeVelmax",100):
			particle.getVelocity()[i] = particle.getParam("rangeVelmax",100)
		elif particle.getVelocity()[i] < particle.getParam("rangeVelmin",0):
			particle.getVelocity()[i] = particle.getParam("rangeVelmin",0)
     
		#Update position
		particle.getPosition()[i] = particle.getPosition()[i] + particle.getVelocity()[i]
 		#Search space limit
		if particle.getPosition()[i] > particle.getParam("rangePosmax",100):
			particle.getPosition()[i] = particle.getParam("rangePosmax",100)
			particle.getVelocity()[i] = particle.getVelocity()[i] * (-1)
		
		elif particle.getPosition()[i] < particle.getParam("rangePosmin",-100):
			particle.getPosition()[i] = particle.getParam("rangePosmin",-100)
			particle.getVelocity()[i] = particle.getVelocity()[i] * (-1)
	
	
def P1DGlobalInfoCommunicator(particle,**args):
	""" Global Communicator -  Update method for particle information (fitness)

		:param particle: the particle to be updated
		
		You must specify the pso_engine parameter with args["pso_engine"] with 
		the :class:`Pso.SimplePSO`  instance.

	"""
	try:
		pso_engine = args["pso_engine"]
	except:
		Util.raiseException("to use the P1DGlobalInfoCommunicator, you must specify the args['topology'] parameter")
	
	if pso_engine.minimax == Consts.minimaxType["maximize"]:
		#update globalParticle information
		
		if (particle.getFitness() > particle.getOwnBestFitness()):
			particle.setOwnBestFitness(particle.getFitness())
			particle.setOwnBestPosition(particle.getPosition())
		
		#update topology swarm information
		if particle.getOwnBestFitness() > pso_engine.topology.getBestParticle().getOwnBestFitness():
			pso_engine.topology.setBestParticle(particle)

	else:
		#update global Particle information
		if (particle.getFitness() < particle.getOwnBestFitness()):
			particle.setOwnBestFitness(particle.getFitness())
			particle.setOwnBestPosition(particle.getPosition())
        #update topology swarm information
		if particle.getOwnBestFitness() < pso_engine.topology.getBestParticle().getOwnBestFitness():
			pso_engine.topology.setBestParticle(particle)