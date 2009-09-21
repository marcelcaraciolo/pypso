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

0.10 2009-09-30 Initial version.
'''

"""

:mod:`Initializators` -- initialization methods module
===================================================================

In this module we have the swarm operators of initialization for each
particle representation, the most part of initialization is done by
choosing random data.

"""

from random import randint as rand_randint, uniform as rand_uniform, choice as rand_choice
import Util

#############################
##     1D Binary String    ##
#############################

def P1DBinaryStringInitializator(vector, **args):
   """ 1D Binary String initializator """
   vector.clearString()
   for i in xrange(len(vector)):
      vector.append(rand_choice((0,1)))

####################
##     1D List    ##
####################

def P1DListInitializatorDimmension(vector, **args):
   """ Dimmension initialization function of Particle1D

   To use this initializator, you must specify the *dimmension* particle parameter with the
   :class:`PsoDimmension.PsoDimmensions` instance.

   """

   dimmension = vector.getParam("dimmension", None)
   if dimmension is None:
      Util.raiseException("to use the P1DListInitializatorDimmension, you must specify the 'dimmension' parameter")

   vector.clearList()
   
   for i in xrange(vector.listSize):
      random_dimmension = dimmension[i].getRandomDimmension()
      vector.append(random_dimmension)

def P1DListInitializatorInteger(vector, **args):
   """ Integer initialization function of Particle1D

   This initializator accepts the *rangemin* and *rangemax* particle parameters.

   """
   vector.clearList()
   
   for i in xrange(vector.listSize):
      randomInteger = rand_randint(vector.getParam("rangemin", 0),
                                   vector.getParam("rangemax", 100))
      vector.append(randomInteger)


def P1DPosListInitializatorReal(vector, **args):
   """ Real  position initialization function of Particle1D

   This initializator accepts the *rangemin* and *rangemax* vector parameters.

   """
   vector.clearList("position")

   for i in xrange(vector.dimmensionsSize):
      randomReal = rand_uniform(vector.getParam("rangePosmin", -100),
                                vector.getParam("rangePosmax", 100))
      vector.append('position',randomReal)


def P1DVelListInitializatorReal(vector, **args):
   """ Real  velocity initialization function of Particle1D

   This initializator accepts the *rangemin* and *rangemax* vector parameters.

   """
   vector.clearList("velocity")

   for i in xrange(vector.dimmensionsSize):
      randomReal = rand_uniform(vector.getParam("rangeVelmin", 0),
                                vector.getParam("rangeVelMax", 100))
      vector.append('velocity',randomReal)
