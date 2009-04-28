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

"""

This module have the Topology Statistics Class. It's responsable to keep
the information about the best particle of the topology at each timeStep
during the evolution proccess. It inherits the Statistics base class.

"""

from pypso import Statistics

class TopologyStatistics(Statistics.Statistics):
    
    #Class Constructor
    def __init__(self):
        #Call the superclass constructor
        super(TopologyStatistics,self).__init__()
        #'fit means  'fitness'
        self.internalDict = {   "bestFitness"   : 0.0,
                                "fitness"       : 0.0,
                                "bestPosition"  : [],
                                "bestPosDim:"   : 0.0,
                                "Position"      : []
                             }
   
        self.descriptions = {   "bestFitness"  : "Best Fitness of the best Particle",
                                "fitness"      : "Fitness of the best Particle",
                                "bestPosition" : "Best Position of the best Particle",
                                "bestPosDim:"  : "Best 1st Dim. Position of the best Particle",
                                "position"     : "Position of the best Particle"
                            } 


    #Return a string representation of the statistics
    def __repr__(self):
        strBuff = "- Best Particle Topology Statistics\n"
        for k,v in self.internalDict.items():
            if type(v) is list:
                strBuff += "\t%-45s = %.2f\n" % (self.descriptions.get(k,k), v)
            else:
                strBuff += "\t%-45s = %s\n" % (self.descriptions.get(k,k), v)
        return strBuff
