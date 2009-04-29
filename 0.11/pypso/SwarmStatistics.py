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

This module contains the  SwarmStatistics class which is responsible 
to keep the statistics of the PSO Swarm. It inherits the base class 
Statistics. Swarm particles statistcs is the main purpose of this class.

"""
from pypso import Statistics

class SwarmStatistics(Statistics.Statistics):
    
    #Class Constructor
    def __init__(self):
        #Call the superclass constructor
        super(SwarmStatistics,self).__init__()
        #'fit means  'fitness'
        self.internalDict = {   "bestFitMax" : 0.0,
                                "bestFitMin" : 0.0,
                                "bestFitAvg" : 0.0,
                                "bestFitDev" : 0.0,
                                "bestFitVar" : 0.0,
                                "fitMin"     : 0.0,
                                "fitMax"     : 0.0,
                                "fitAvg"     : 0.0
                             }
   
        self.descriptions = {   "bestFitMax" : "Maximum best Fitness",
                                "bestFitMin" : "Minimum best Fitness",
                                "bestFitAvg" : "Average of best Fitness",
                                "bestFitDev" : "Standard deviation of best Fitness",
                                "bestFitVar" : "Best Fitness variance",
                                "fitMin" : "Minimum fitness",
                                "fitMax" : "Maximum fitness",
                                "fitAvg" : "Fitness average" 
                            } 
    
        #Return a string representation of the statistics
    def __repr__(self):
        strBuff = "-Statistics\n"
        for k,v in self.internalDict.items():
            strBuff += "\t%-45s = %.2f\n" % (self.descriptions.get(k,k), v)
        return strBuff
    

