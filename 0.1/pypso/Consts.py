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

"""     This module contains all default settings and constants, to help the user 
        in the API to use and minimize the source code need to make simple
        things. You are encouraged to see the constants, but NOT CHANGE DIRECTLY
        on the module. There are methods for this.

"""




#Required python version 2.5+
CDefPythonRequire = (2,5)

CDefESCKey = 27

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

#Default Topology
CDefTopology = None

#Default Time Steps
CDefSteps = 1000

#Position and Velocity Bounds
initialPositionBounds = []
positionBounds = []
velocityBounds = []

#Inertia constants
CDefInertiaFactorStart = 0.9
CDefInertiaFactorEnd = 0.4


# Optimization type
# - Minimize or Maximize the Evaluator Function
minimaxType = { "minimize" : 0,
                "maximize" : 1
               }
#Social and Cognitive Coefficients (C1 and C2)
CDefCoefficients = (2.05,2.05)
