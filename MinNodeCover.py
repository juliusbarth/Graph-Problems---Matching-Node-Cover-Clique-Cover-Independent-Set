# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 11:06:30 2020

@author: jfb2444
"""

import matplotlib.pyplot as plt
import networkx as nx
import gurobipy as gp
from gurobipy import GRB

def runMinNodeCover(adjMatrix):
    
    # Create a new model
    print("\n-----------------------------")
    print("\nBuilding Model: Node Cover")
    model = gp.Model("NodeCover_Model")
    model.Params.OutputFlag = 1
    
    nbNodes = len(adjMatrix[0])
    Nodes = range(0,nbNodes)
    
    # Create variables
    x = model.addVars(Nodes, vtype=GRB.BINARY, obj=1, name="var_NodeSelection")
    
    # Define objective function direction
    model.modelSense = GRB.MINIMIZE
    
    # Define Constraints
    # Cover constraint for each edge
    for i in range(0,nbNodes-1):
            for j in range(i+1,nbNodes):
                if adjMatrix[i][j] == 1:
                    model.addConstr( x[i] + x[j] >= 1 , "ct_Edge[%s,%s]" % (i,j) )
    
    # Optimize the model
    print("\nOptimizing")
    model.optimize()
    
    print("\nPostprocessing") # Check if feasible solution was found
    status=model.status
    if status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
        objVal = model.getObjective().getValue()
        print("Cardinality of Minimum Node Cover:", objVal)
        G_01 = nx.from_numpy_matrix(adjMatrix)
        minNodeCover = set()
        color = ['grey' for i in Nodes]
        for i in Nodes:
            if x[i].x == 1:
                minNodeCover.add(i)
                color[i] = 'green'
                #print('Node', i, ':', x[i].x)   
        plt.figure('MinNodeCover')                
        nx.draw_circular(G_01, with_labels=True, node_color = color)
        plt.figure('MinNodeCover').savefig('MinNodeCover.png')
        
        return minNodeCover
        
        