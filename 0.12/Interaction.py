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

0.10 2009-04-29 Initial version.
'''

"""

:mod:`Interaction` -- interaction module
==========================================================================

In this module, you will find the funcionality for the :term:`Interactive mode`.
When you enter in the Interactive Mode, PyPso will automatic import this module
and exposes to you in the name space called "it".

To use this mode, the parameter *interactiveMode* must be enabled in the
:class:`Pso.SimplePSO`.

"""
import Util

try:
   print "Loading module pylab (matplotlib)...",
   import pylab
   print " done!"
except:
   print "\nWarning: cannot import Matplotlib ! Plots will not be available !"

try:
   print "Loading module numpy...",
   import numpy
   print " done!"
except:
   print "\nWarning: cannot import Numpy ! Some functions will not be available !"
   

def getSwarmFitness(topology, bestFitness=False):
    """ Returns a list of swarm fitness scores
        Example:
            >>> lst = Interaction.getSwarmFitness(topology)
            
        :param topology: the swarm object
        :param bestFitness: If it's True, the best fitness will be used, otherwise, the current one.
        :rtype: the list of the swarm fitness
    """
    fitness_list = []
    for particle in topology:
        if bestFitness:
            x = particle.ownBestFitness
        else:
            x = particle.fitness
        fitness_list.append(x)
    return fitness_list


def getSwarmPosition(topology, bestPosition=False):
    """ Returns a list of swarm particles positions (2 dimmensions)
        Example:
            >>> lst = Interaction.getSwarmPosition(topology)
            
        :param topology: the swarm object
        :param bestFitness: If it's True, the best position will be used, otherwise, the current one.
        :rtype: the list of the swarm positions
    """
    position_list = []
    flag = False
    for particle in topology:
        if particle == topology.getBestParticle():
            flag = True
        if bestPosition:
            x = particle.ownBestPosition[:2]
        else:
            x = particle.position[:2]
        if flag:
            position_list.insert(0,tuple(x))
            flag = False
        else:
            position_list.append(tuple(x))
    return position_list


def plotSwarmFitness(topology, bestFitness=False):
    """ Plot the swarm fitness distribution 
        Example:
            >>> Interaction.plotSwarmFitness(topology)

   :param topology: topology object subclass of (:class:`TopologyBase.TopologyBase`)
   :param bestFitness: If it's True, the bestFitness score will be used, otherwise, the current one.
   :rtype: None

    """
    fitness_list = getSwarmFitness(topology,bestFitness)
    pylab.plot(fitness_list,'o')
    pylab.title("Plot of the swarm fitness distribution")
    pylab.xlabel('Particle')
    pylab.ylabel('Fitness')
    pylab.grid(True)
    pylab.show()


def plotHistSwarmFitness(topology, bestFitness=False):
    """ Swarm fitness distribution histogram 

       Example:
          >>> Interaction.plotHistSwarmFitness(topology)

   :param topology: topology object subclass of (:class:`TopologyBase.TopologyBase`)
   :param bestFitness: If it's True, the bestFitness score will be used, otherwise, the current one.
   :rtype: None
   
   """
    fitness_list = getSwarmFitness(topology,bestFitness)
    n,bins,patches = pylab.hist(fitness_list,50,facecolor='green',alpha=0.75,normed=1)
    pylab.plot(bins,pylab.normpdf(bins,numpy.mean(fitness_list),numpy.std(fitness_list)),'r--')
    pylab.xlabel('Fitness')
    pylab.ylabel('Frequency')
    pylab.grid(True)
    pylab.title("Plot of the swarm fitness distribution")
    pylab.show()

def plotSwarmPosition(topology,bestPosition=False):
    """ Plot the swarm position distribution (2D Dimension)

       Example:
          >>> Interaction.plotSwarmPosition(topology)

   :param topology: topology object subclass of (:class:`TopologyBase.TopologyBase`)
   :param bestPosition: f it's True, the bestPosition will be used, otherwise, the current one.
   :rtype: None
   
   """
    position_list = getSwarmPosition(topology,bestPosition)
    x_list = []
    y_list = []
    print position_list
    for x,y in position_list[1:]:
        x_list.append(x)
        y_list.append(y)
    pylab.plot(x_list,y_list,'o')
    pylab.plot([position_list[0][0]],[position_list[0][1]],'ro')
    pylab.title("Plot of the swarm  particles position distribution")
    pylab.xlabel('X')
    pylab.ylabel('Y')
    pylab.grid(True)
    pylab.show()