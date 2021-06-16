# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 23:03:56 2020

@author: jfb2444
"""

import matplotlib.pyplot as plt
import networkx as nx
import gurobipy as gp
from gurobipy import GRB

def runMaxIndependentSet(adjMatrix, adjMatrix_Comp):
          
    # Create a new model
    print("\n-----------------------------")
    print("Building Model: Independent Set")
    model = gp.Model("IndependentSetProblem_Model")
    model.Params.OutputFlag = 1
    
    nbNodes = len(adjMatrix[0])
    Nodes = range(0,nbNodes)
    
    # Create variables
    x = model.addVars(Nodes, vtype=GRB.BINARY, obj=1, name="var_NodeSelection")
    
    # Define objective function direction
    model.modelSense = GRB.MAXIMIZE
    
    # Define Constraints
    # Stability constraint
    for i in range(0,nbNodes-1):
        for j in range(i+1,nbNodes):
            if adjMatrix[i][j] == 1:
                model.addConstr( x[i] + x[j] <= 1 , "ct_Edge[%s,%s]" % (i,j) )
    
    print("\nOptimizing")
    # Optimize the model
    model.optimize()
    
    print("\nPostprocessing") # Check if feasible solution was found
    status=model.status
    if status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
        objVal = model.getObjective().getValue()
        print("Cardinality of Maximum Independent Set:", objVal)
        G_01 = nx.from_numpy_matrix(adjMatrix)
        G_01_Comp = nx.from_numpy_matrix(adjMatrix_Comp)
        maxIndependentSet = set()
        color = ['grey' for i in Nodes]
        color_Comp = ['grey' for i in Nodes]
        for i in Nodes:
            if x[i].x == 1:
                maxIndependentSet.add(i)
                color[i] = 'green'
                color_Comp[i] = 'green'
                #print('Node', i, ':', x[i].x)           
        plt.figure('MaxIndSet')
        nx.draw_circular(G_01, with_labels=True, node_color = color)
        plt.figure('MaxIndSet').savefig('IndependentSet.png')
        plt.figure('CliqueInCompGraph')
        nx.draw_circular(G_01_Comp, with_labels=True, node_color = color)
        plt.figure('CliqueInCompGraph').savefig('CliqueInCompGraph.png')
        
        
        return maxIndependentSet