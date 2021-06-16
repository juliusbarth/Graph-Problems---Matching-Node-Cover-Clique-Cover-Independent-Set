# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 18:08:11 2020

@author: jfb2444
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx

def generateData(nbNodes, density, seed):
    print("\nGenerating Random Graph\n")
    
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Graph data (Assumption: Graph is connected)
    Nodes = range(0,nbNodes)
    adjMatrix = np.zeros((nbNodes, nbNodes))
    adjMatrix_Comp = np.zeros((nbNodes, nbNodes))
    degree = [0 for i in Nodes]
    
    connected = False
    while connected == False:
        for i in range(0,nbNodes-1):
            for j in range(i+1,nbNodes):
                if random.uniform(0, 1) <= density:
                    adjMatrix[i][j] = 1
                    adjMatrix_Comp[i][j] = 0
                    degree[i] = degree[i] + 1
                    degree[j] = degree[j] + 1
                else:
                    adjMatrix[i][j] = 0
                    adjMatrix_Comp[i][j] = 1
            #print(adjMatrix[i][:])
            G = nx.from_numpy_matrix(adjMatrix)
            connected = nx.is_connected(G)
            
    #Plot original and complement graph        
    G = nx.from_numpy_matrix(adjMatrix) 
    G_Comp = nx.from_numpy_matrix(adjMatrix_Comp) 
    plt.figure('Graph G')
    nx.draw_circular(G, with_labels=True)
    
    plt.figure('Complement')
    nx.draw_circular(G_Comp, with_labels=True)
    
    return adjMatrix, adjMatrix_Comp
