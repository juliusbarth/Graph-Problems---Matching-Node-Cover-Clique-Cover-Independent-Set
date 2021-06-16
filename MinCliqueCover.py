# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 23:04:46 2020

@author: jfb2444
"""

import math
import matplotlib.pyplot as plt
import networkx as nx
import gurobipy as gp
from gurobipy import GRB

def runMinCliqueCover(adjMatrix, symmetryBreaking, dualBound, maxStableSet):
    
    # Create a new model
    print("\n-----------------------------")
    print("Building Model: Clique Cover")
    model = gp.Model("CliqueCoverProblem_Model")
    model.Params.OutputFlag = 1
    
    maxStableSetCardinality = len(maxStableSet)
    
    nbNodes = len(adjMatrix[0])
    Nodes = range(0,nbNodes)
    
    G_02 = nx.from_numpy_matrix(adjMatrix) 
    if nx.is_connected(G_02) == True:
        nbCliques = math.ceil(nbNodes/2)
    else: 
        nbCliques = nbNodes
    Cliques = range(0,nbCliques)
    
    # Create variables
    x = model.addVars(Cliques, vtype=GRB.BINARY, obj=1, name="var_Clique")
    y = model.addVars(Nodes, Cliques, vtype=GRB.BINARY, obj=0, name="var_Assignment")
    
    # Define objective function direction
    model.modelSense = GRB.MINIMIZE
    
    # Define Constraints
    # Node-Clique Indicator Constraint
    for i in Nodes:
        for l in Cliques:
            model.addConstr( y[i,l] <=  x[l] , "ct_NodeClique[%s,%s]" % (i,l) )
    
    # Clique Connectivity Constraint
    for i in range(0,nbNodes-1):
        for j in range(i+1,nbNodes):
            if(adjMatrix[i][j] != 1):
                for l in Cliques:
                    model.addConstr( y[i,l] + y[j,l] <=  1 , "ct_CliqueConn[%s,%s,%s]" % (i,j,l) )
    
    # Node Assignment Constraint
    for i in Nodes:
        model.addConstr( sum(y[i,l] for l in Cliques) ==  1 , "ct_NodeAssign[%s]" % (i) )
    
    # Symmetry Breaking Constraint: Assign elements of maximum stable set to different cliques
    if(symmetryBreaking == True):
        k = 0
        for i in maxStableSet:
            model.addConstr(y[i,k] == 1)
            k = k+1
    
    # Lower Bound from Duality
    if(dualBound == True):
        model.addConstr( sum(x[l] for l in Cliques) >=  maxStableSetCardinality , "ct_DualBound[%s]" )
    
    print("\nOptimizing")
    # Optimize the model
    model.optimize()   
    
    print("\nPostprocessing") # Check if feasible solution was found
    status=model.status
    if status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
        objVal = model.getObjective().getValue()
        print("Cardinality of Minimum Clique Covering:", objVal)
        
        G_02 = nx.from_numpy_matrix(adjMatrix)    
        color = [0 for i in Nodes]
        for l in Cliques:
            for i in Nodes:
                if y[i,l].x == 1:
                    color[i] = l
                    #print('Node ', i, '\t in Clique', l)           
        plt.figure('MinCliqueCover')
        nx.draw_circular(G_02, with_labels=True, node_color = color)
        plt.figure('MinCliqueCover').savefig('CliqueCover.png')
        
        return objVal