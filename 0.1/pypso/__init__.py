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

'''
    This is the main module of pypso, every other module is above this
    namespace, for example, to import module Topology:
      >> from pypso import Topology
'''

__version__ = "0.1"
__author__ = "Marcel Pinheiro Caraciolo"

import Consts
import sys

if sys.version_info < Consts.CDefPythonRequire:
    raise Exception("Python 2.5+ required!")
else:
    del sys

