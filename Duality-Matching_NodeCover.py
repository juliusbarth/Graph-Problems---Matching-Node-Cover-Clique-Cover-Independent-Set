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
nbNodes = 15
density = 0.2
adjMatrix = generateData(nbNodes, density)
    
# Max Matching
maxMatchingCardinality = runMaxMatching(adjMatrix)

# Min Node Cover    
runMinNodeCover(adjMatrix)    
       






