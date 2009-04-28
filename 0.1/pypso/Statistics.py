
#                       The evolutionary statistics (Info bout the best particle)
#                       THe Simulation statistics (Info about all the simulation)
#  Info about the boxPlot, Emanoel analysis and convergence rate, avg, dev, var.
#

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

This module have the class which is responsible to keep the statistics of 
the PSO. This is  the main class which must BE INHERITED by the other statistic
dump classes


"""

import Consts

#Statistics Class - A class bean-like to store the statistics
class Statistics(object):

    #'fit' means 'fitness'
    def __init__(self):
        self.internalDict = {}
        self.descriptions = {}
        
    #Return the specific statistics by key
    def __getitem__(self,key):
        return self.internalDict[key]
    
    #set the statistic
    def __setitem__(self,key,value):
        self.internalDict[key] = value
   
    #Return the length of internal stats dictionary
    def __len__(self):
        return len(self.internalDict)
    
    #Return a string representation of the statistics
    def __repr__(self):
        strBuff = "-Statistics\n"
        for k,v in self.internalDict.items():
            strBuff += "\t%-45s = %.2f\n" % (self.descriptions.get(k,k), v)
        return strBuff
    
    #Returns the stats as a python tuple 
    def asTuple(self):
        return tuple(self.internalDict.values())

    def clear(self):
        for k in self.internalDict.keys():
            self.internalDict[k] = 0

    #Return a tuple (name,value) for all stored statistics
    def items(self):
        return self.internalDict.items()

      