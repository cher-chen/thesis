#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 20:22:53 2020

@author: cherc
"""

# =============================================================================
# optimal model
# objective: Maximize minimum benefit
# =============================================================================

from gurobipy import *
from time import process_time

    
def MILPmodel(Nmachines, Njobs, p, s, b, h, penalty = 1):
    
    machines = range(1, Nmachines+1)
    jobs = range(1, Njobs+1)
    jobs0 = range(Njobs+1)

    start = process_time()
    
    V = 99999
        
    ## Create a new model
    model = Model("model1")
    
    
    ## Create variables
    # job j before job k on machine i
    x = model.addVars(machines, jobs0, jobs0, vtype = GRB.BINARY, name = "x")
    # job j on machine i
    y = model.addVars(machines, jobs0, vtype=GRB.BINARY, name = "y")
    # completion time
    w = model.addVars(jobs0, vtype = GRB.CONTINUOUS, name = "w") 
    # maximize value
    z = model.addVar(vtype = GRB.CONTINUOUS, name = "z")
    # overtime 
    o = model.addVars(machines, vtype = GRB.CONTINUOUS, name = "o")
    

    ## Add constraints
    # a job is before job k
    model.addConstrs((quicksum(x[i, j, k] for i in machines for j in jobs0)== 1 for k in jobs), "c1") 
    # a job is after job j
    model.addConstrs((quicksum(x[i, j, k] for i in machines for k in jobs0)== 1 for j in jobs), "c2")
    # only one job is the first
    model.addConstrs((quicksum(x[i, 0, k] for k in jobs) <= 1 for i in machines), "c3")
    # one is before one is after
    model.addConstrs((quicksum(x[i, j, k] for k in jobs0) - quicksum(x[i, f, j] for f in jobs0) == 0 for i in machines for j in jobs), "c4")
    # relations between x and y
    model.addConstrs((x[i, j, k] <= y[i, j] for i in machines for j in jobs0 for k in jobs), "c5") 
    model.addConstrs((x[i, j, k] <= y[i, k] for i in machines for j in jobs0 for k in jobs), "c6")
    model.addConstrs((y[i, j] <= quicksum(x[i, j, k] for k in jobs0) for i in machines for j in jobs0), "c7")
    # ensure the processing order and jobs are non-preemptive
    model.addConstrs((w[k] - w[j] + V * (1 - x[i, j, k]) >= s[i, j, k] + p[i, k] for i in machines for j in jobs0 for k in jobs if j != k), "c8")
    # ensures the capacity limit of each machine
    #model.addConstrs((w[j] <= h[i] for i in machines for j in jobs), "c8-1")
    #### model.addConstrs((w[j] <= h[i] + o[i] for i in machines for j in jobs), "c8-1")
    #model.addConstrs((quicksum((s[i, j, k] + p[i, k]) * x[i, j, k] for j in jobs for k in jobs) <= h[i] for i in machines), "c8-2")
    model.addConstrs((quicksum((s[i, j, k] + p[i, k]) * x[i, j, k] for j in jobs for k in jobs) <= h[i] + o[i] for i in machines), "c9")
    model.addConstrs((o[i] >= 0 for i in machines), "c10")
    # dummy job completes at time 0
    model.addConstr((w[0] == 0), "c11")
    # completion time of each job should be positive
    model.addConstrs((w[j] >= 0 for j in jobs), "c12")
    # minimum benefit among all machines
    # model.addConstrs((z <= quicksum(b[i,j] * y[i,j] for j in jobs) for i in machines), "c12")
    model.addConstrs((z <= quicksum(b[i,j] * y[i,j] for j in jobs) - o[i] * penalty for i in machines), "c13")
    model.addConstrs((x[i, j, j] == 0 for i in machines for j in jobs0), "c14")
    
    
    #update model
    model.update()
    
    # Set objective
    model.setObjective(z, GRB.MAXIMIZE)
    
    
    # Optimize model
    model.optimize()


    end = process_time()
    
    return model.objVal, end - start

