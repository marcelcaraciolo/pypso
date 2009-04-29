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

#Pso Demo

from pypso import Pso
from pypso import Consts
from pypso import GlobalTopology

#This is the Sphere Function
def sphere(position):
    n = len(position)
    total = 0.0
    for i in xrange(n):
        total += (position[i] ** 2.0)
    return total

#Parameters
dimensions = 30
swarm_size = 30
timeSteps = 10000

# PSO Instance

pso = Pso.PSO()
pso.setPsoType(Consts.psoType["CONSTRICTED"])
pso.setTimeSteps(timeSteps)
pso.setTopology(GlobalTopology.GlobalTopology(swarm_size,dimensions))

# The evaluator function (objective function)
pso.setFunction(sphere)
pso.initializeBounds(dimensions)
pso.definePositionBounds(0, dimensions, (-100.0, 100.0))
pso.defineInitialPositionBounds(0,dimensions, (50.0,100.0))
pso.defineVelocityBounds(0,dimensions,100.0)

#Do the swarm movement, with stats
#dump frequency of 10 timeSteps
import psyco

psyco.full()

pso.execute(freq_stats=20)






