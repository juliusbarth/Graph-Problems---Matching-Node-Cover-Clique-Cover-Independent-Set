# -*- coding: utf-8 -*-
"""
Created on Tue May 12 22:08:55 2020

@author: jfb2444
"""

###############################################################################
################################  Imports #####################################
###############################################################################
from datetime import datetime
from DataGeneration import generateData
from MaxIndependentSet import runMaxIndependentSet
from MinCliqueCover import runMinCliqueCover
from MinNodeCover import runMinNodeCover
from MaxMatching import runMaxMatching

# Pseudoclear console
for i in range(25):
    print("")
dateTimeObj = datetime.now()
print("New run @", dateTimeObj)

###############################################################################
################################  Data ########################################
###############################################################################
nbNodes = 10
density = 0.4
seed = 10
adjMatrix, adjMatrix_Comp = generateData(nbNodes, density, seed)

###############################################################################
################################  Optimization ################################
###############################################################################

''' 
Relationships:

- Maximum Matching          &   Minimum Node Cover      are Dual to each other
- Maximum Independent Set   &   Minimum Clique Cover    are Dual to each other
- Maximum Independent Set = {All Vertices} \ {Minimum Node Cover}
    
'''

# Optimize Maximum Matching Problem
maxMatchingCardinality = runMaxMatching(adjMatrix)

# Optimize Minimum Node Cover Problem
minNodeCover = runMinNodeCover(adjMatrix)
minNodeCover = len(minNodeCover)

# Optimize Maximum Stable Set Problem
maxIndependentSet = runMaxIndependentSet(adjMatrix, adjMatrix_Comp)
maxIndependentSetCardinality = len(maxIndependentSet)
   
# Optimize Minimum Clique Cover Problem
dualBound = True
minCliqueCoverCardinality = runMinCliqueCover(adjMatrix, False, False, maxIndependentSet)

