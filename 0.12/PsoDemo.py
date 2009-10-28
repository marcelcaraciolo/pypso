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
0.20 2009-05-21 Added support for demonstration of Local Topology.
0.21 2009-05-26 Added support for report generation(CSV File).
0.22 2009-05-28 Added support for report generation (database SQLite).
0.23 2009-09-09 Added support for the new API and docs.
'''

""""
PSO Demo - Used for Minimization of the Sphere Function

"""

#from pypso import Particle1D
import Particle1D
import GlobalTopology
import Pso
import Consts
import ReportAdapters

#This is the Sphere Function

def sphere(particle):
	total = 0.0
	for value in particle.position:
		total += (value ** 2.0)
	
	return total


#Parameters
dimensions = 30
swarm_size = 30
timeSteps = 10000

# Particle Representation
particleRep = Particle1D.Particle1D(dimensions)

#The evaluator function(objective function)
particleRep.evaluator.set(sphere)

#Set the range for initialization
particleRep.setParams(rangePosmin=-100.0,rangePosmax=100.0)
particleRep.setParams(rangeVelmin=-100.0, rangeVelmax=100.0)

#PSO instance
topology = GlobalTopology.GlobalTopology(particleRep)
#print topology
pso = Pso.SimplePSO(topology)
pso.setTimeSteps(timeSteps)
pso.setPsoType(Consts.psoType["CONSTRICTED"])

#Report Sqlite3 Db adapter instance
sqlite_adapter = ReportAdapters.ReportDB(dbname='simulationPso2.db',identify="ex2",resetIdentify=False,resetDB=False)
pso.setReportAdapter(sqlite_adapter)

#Do the swarm movement, with stats
#dump frequency of 10 timeSteps
pso.execute(freq_stats=20)

#Best particle
#print pso.bestParticle()

