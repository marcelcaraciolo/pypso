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
0.11 2009-05-25 Added constants for ReportFileCSV Adapter (Reports).
0.12 2009-05-28 Added constants for ReportDB Adapter (Reports).
0.23 2009-09-09 Redesigned constants for new API and Docs.

'''

"""    
	:mod `Consts``-- constants module
	
	This module contains all default settings and constants, to help the user 
	in the API to use and minimize the source code need to make simple
    things. You are encouraged to see the constants, but NOT CHANGE DIRECTLY
    on the module. There are methods for this.



General constants
----------------------------------------------------------------------------

.. attribute:: CDefPythonRequire
  
   The mininum version required to run Pyevolve.

.. attribute:: minimaxType

  The Min/Max type, maximize or minimize the evaluation function.

  Example:
     >>> minmax = Consts.minimaxType["minimize"]
     >>> minmax = Consts.minimaxType["maximize]
     
.. attribute:: CDefESCKey

   The ESC key ASCII code. Used to start Interactive Mode.

TopologyBase constants (:class:`TopologyBase.TopologyBase`)
----------------------------------------------------------------------------

.. attribute:: CDefSwarmSortType

	Default sort type parameter.

.. attribute:: CDefSwarmMinimax

   Default min/max parameter.

.. attribute:: CDefSwarmScale

   Default scaling scheme.


1D List particle constants (:class:`Particle1D.Particle1D`)
----------------------------------------------------------------------------

.. attribute:: CDefP1PosDListInit

   Default initializator for the 1D  position List particle.

.. attribute:: CDefP1DVelListInit

   Default initializator for the 1D velocity List particle.

.. attribute:: CDefP1DInfoCommunicator

   Default initializator for the particle information communicator

.. attribute:: CDefP1DPosCommunicator

   Default initializator for the particle position communicator



PSO Engine constants (:class:`PSO.SimplePSO`)
----------------------------------------------------------------------------

.. attribute:: CDefSteps

   Default number of steps.

.. attribute:: CDefCoefficients

   Default social and cognitive coefficients (C1 and C2).

.. attribute:: CDefPsoType

   Default PSO type (Basic, Inertia or Constricted).

.. attribute:: CDefSwarmSize

   Default swarm size.

Report Adapters constants (:mod:`ReportAdapters`)
----------------------------------------------------------------------------
Constants for the Report Adapters

SQLite3 Report Adapter Constants (:class:`ReportAdapters.ReportDB`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. attribute:: CDefDBName
   
   Default database filename.

.. attribute:: CDefReportDBSwarmTable

   Default swarm statistical table name.

.. attribute:: CDefReportDBTopTable

   Default topology statistical table name.


.. attribute:: CDefSQLiteDBPartTable

   Default particles statistical table name.


.. attribute:: CDefDBStatsGenFreq

   Default generational frequency for dump statistics.

.. attribute:: CDefDBStatsCommitFreq

   Default commit frequency.


CSV File DB Adapter Constants (:class:`ReportAdapters.ReportFileCSV`)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. attribute:: CDefCSVFileName
   
   The default CSV filename to dump statistics.

.. attribute:: CDefCSVFileStatsGenFreq

   Default generational frequency for dump statistics.


"""

import Initializators
import Communicators


# Types of sort
# - fitness: uses the "score" attribute
# - bestFitness: uses the "fitness" attribute
sortType = { 
   "fitness"    : 0,
   "bestFitness" : 1
}

#Required python version 2.5+
CDefPythonRequire = (2,5)


CDefESCKey = 27


# - Particle1D defaults

CDefP1DPosListInit      = Initializators.P1DPosListInitializatorReal
CDefP1DVelListInit      = Initializators.P1DVelListInitializatorReal
P1DInfoCommunicator =  Communicators.P1DGlobalInfoCommunicator
P1DPosCommunicator = Communicators.P1DGlobalPosCommunicator

#PSO Engine defaults

# Types of Pso Evaluation
# - BASIC: the canonical PSO Algorithm
# - INERTIA: The Inertia coefficient factor PSO Algorithm
# - CONSTRICTED: The Constriction factor PSO Algorithm
psoType = { 
   "BASIC"    : 0,
   "INERTIA" : 1,
   "CONSTRICTED" : 2
}

#Default PsoType
CDefPsoType  = psoType["BASIC"]

#Default Time Steps
CDefSteps = 1000

# Optimization type
# - Minimize or Maximize the Evaluator Function
minimaxType = { "minimize" : 0,
                "maximize" : 1
               }
#Social and Cognitive Coefficients (C1 and C2)
CDefCoefficients = (2.05,2.05)


# - TopologyBase Defaults
CDefSwarmSortType               = sortType["fitness"]
CDefSwarmMinimax                = minimaxType["minimize"]
CDefSwarmSize 					= 30


# - Report Adapters CSV File defaults
CDefCSVFileName = "pypso.csv"
CDefCSVFileStatsGenFreq = 1

# - DB Adapters defaults
CDefDBName = "simulationPSO.db"
CDefReportDBSwarmTable = "swarm"
CDefReportDBTopTable = "topology"
CDefSQLiteDBPartTable = "particles"
CDefDBStatsGenFreq = 1
CDefDBStatsCommitFreq = 500