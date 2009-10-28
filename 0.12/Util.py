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
0.23 2009-09-30 Changed for support generic pso and docs.
'''

"""

:mod:`Util` -- utility module
============================================================================

This is the utility module, with some utility functions of general
use, like list item swap, random utilities and etc.

"""

def raiseException(message, expt=None):
	"""
	Raise an exception
	Example:
		>>> Util.raiseException("The value is not an integer", ValueError)
		
	:param message : the message of the exception
	:param expt: the exception class
	:rtype None
	
	"""
	if expt is None:
		raise Exception(message)
	else:
		raise expt, message

