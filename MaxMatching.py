# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 11:06:52 2020

@author: jfb2444
"""

import matplotlib.pyplot as plt
import networkx as nx
import gurobipy as gp
from gurobipy import GRB

def runMaxMatching(adjMatrix):
    
    # Create a new model
    print("\n-----------------------------")
    print("\nBuilding Model: Matching")
    model = gp.Model("Matching_Model")
    model.Params.OutputFlag = 1
    
    nbNodes = len(adjMatrix[0])
    Nodes = range(0,nbNodes)  
    
    Edges = set()
    for i in range(0,nbNodes-1):
        for j in range(i+1,nbNodes):
            if adjMatrix[i][j] == 1:
                tmpTuple = (i, j)
                Edges.add(tmpTuple)
            
    # Create variables
    x = model.addVars(Edges, vtype=GRB.BINARY, obj=1, name="var_EdgeSelection")
    
    # Define objective function direction
    model.modelSense = GRB.MAXIMIZE
    
    # Define Constraints
    # Matching constraint for each node
    for i in Nodes:
        model.addConstr( sum(x[i,j] for j in Nodes if j > i and (i,j) in Edges) +
                        sum(x[j,i] for j in Nodes if j < i and (j,i) in Edges) <= 1 , "ct_Matching[%s]" % (i) )    
        
    # Optimize the model
    print("\nOptimizing")
    model.optimize()
    model.write("out.sol")
    
    print("\nPostprocessing") # Check if feasible solution was found
    status=model.status
    if status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
        objVal = model.getObjective().getValue()
        print("Cardinality of Maximum Matching:", objVal)
        G_02 = nx.from_numpy_matrix(adjMatrix) 
        color = [1 for i in Nodes]
        for e in Edges:
            i = e[0]
            j = e[1]
            if x[i,j].x == 1:
                color[i] = e[1]
                color[j] = e[1]
                #print('Node', i, '& Node', j, 'are matched: ', x[i,j].x)           
        plt.figure('MaxMatching')
        nx.draw_circular(G_02, with_labels=True, node_color = color) 
        plt.figure('MaxMatching').savefig('Matching.png')        
        
    return objVal    