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

# Pseudoclear console
for i in range(25):
    print("")
dateTimeObj = datetime.now()
print("New run @", dateTimeObj)

# Optimization Settings
dualBound = True
symmmetryBreaking = True

###############################################################################
################################  Data ########################################
###############################################################################
nbNodes = 70
density = 0.3
adjMatrix = generateData(nbNodes, density)


###############################################################################
################################  Optimization ################################
###############################################################################
# Optimize Maximum Stable Set Problem
maxStableSet = runMaxIndependentSet(adjMatrix)
maxStableSetCardinality = len(maxStableSet)
   
# Optimize Minimum Clique Cover Problem
minCliqueCoverCardinality = runMinCliqueCover(adjMatrix, symmmetryBreaking, dualBound, maxStableSet)
