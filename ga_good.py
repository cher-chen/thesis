#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 17:04:42 2020

@author: cherc
"""

# =============================================================================
# GA try: allow overtime and give overtime penalty to benefit
# 寫成可以用 boolean 的有彈性的 GA
# update initial pool generation method: sorted by cp value first, then random insert
# update initial pool generation method: 用 LPT/CHBF 生一個解
# sorted jobs by benefit, then assign job to the machine with minimum benefit
# =============================================================================


import numpy as np
import random
from random import shuffle
from itertools import combinations



def pickparent(pressure, individuals, benefits, pick1chosen):
    sample_indvs = random.sample([i for i in range(len(individuals))], int(pressure * len(individuals)))
    maxbenefit = 0
    pick = 0 
    for indv in sample_indvs:
        if indv == pick1chosen:
            continue  
        curb = min(benefits[indv])
        if curb > maxbenefit:
            maxbenefit = curb
            pick = indv
   
    return pick

def shiftMutation(offspring, offsptime, offsbenefits, Nmachines, s, h, penalty):  
    #do shift mutation for offspring
    while True:
        mu_machine = random.randint(0, Nmachines-1)
        len_mu_machine = np.where(offspring[mu_machine] == 0)[0][0]
        if len_mu_machine >= 2:
            break
                      
    jobrange = list(range(len_mu_machine))
    ori_pos = random.choice(jobrange)
    jobrange = list(range(0, ori_pos)) + list(range(ori_pos+1, len_mu_machine))
    dest_pos = random.choice(jobrange)
   
    # update ptime
    if ori_pos == 0:
        offsptime[mu_machine] = offsptime[mu_machine] \
        - s[mu_machine+1, 0, offspring[mu_machine][ori_pos]] \
        - s[mu_machine+1, offspring[mu_machine][ori_pos], offspring[mu_machine][ori_pos+1]] \
        - s[mu_machine+1, offspring[mu_machine][dest_pos-1], offspring[mu_machine][dest_pos]] \
        - s[mu_machine+1, offspring[mu_machine][dest_pos], offspring[mu_machine][dest_pos+1]] 
    elif dest_pos == 0:
        offsptime[mu_machine] = offsptime[mu_machine] \
        - s[mu_machine+1, offspring[mu_machine][ori_pos-1], offspring[mu_machine][ori_pos]] \
        - s[mu_machine+1, offspring[mu_machine][ori_pos], offspring[mu_machine][ori_pos+1]] \
        - s[mu_machine+1, 0, offspring[mu_machine][dest_pos]] \
        - s[mu_machine+1, offspring[mu_machine][dest_pos], offspring[mu_machine][dest_pos+1]] 
        
    else:
        offsptime[mu_machine] = offsptime[mu_machine] \
        - s[mu_machine+1, offspring[mu_machine][ori_pos-1], offspring[mu_machine][ori_pos]] \
        - s[mu_machine+1, offspring[mu_machine][ori_pos], offspring[mu_machine][ori_pos+1]] \
        - s[mu_machine+1, offspring[mu_machine][dest_pos-1], offspring[mu_machine][dest_pos]] \
        - s[mu_machine+1, offspring[mu_machine][dest_pos], offspring[mu_machine][dest_pos+1]] 

    # update mutation of offspring1
    offspring[mu_machine][ori_pos], offspring[mu_machine][dest_pos] = \
    offspring[mu_machine][dest_pos], offspring[mu_machine][ori_pos]
    
    # update ptime
    if ori_pos == 0:
        offsptime[mu_machine] = offsptime[mu_machine] \
        + s[mu_machine+1, 0, offspring[mu_machine][ori_pos]] \
        + s[mu_machine+1, offspring[mu_machine][ori_pos], offspring[mu_machine][ori_pos+1]] \
        + s[mu_machine+1, offspring[mu_machine][dest_pos-1], offspring[mu_machine][dest_pos]] \
        + s[mu_machine+1, offspring[mu_machine][dest_pos], offspring[mu_machine][dest_pos+1]] 
    elif dest_pos == 0:
        offsptime[mu_machine] = offsptime[mu_machine] \
        + s[mu_machine+1, offspring[mu_machine][ori_pos-1], offspring[mu_machine][ori_pos]] \
        + s[mu_machine+1, offspring[mu_machine][ori_pos], offspring[mu_machine][ori_pos+1]] \
        + s[mu_machine+1, 0, offspring[mu_machine][dest_pos]] \
        + s[mu_machine+1, offspring[mu_machine][dest_pos], offspring[mu_machine][dest_pos+1]] 
    else:
        offsptime[mu_machine] = offsptime[mu_machine] \
        + s[mu_machine+1, offspring[mu_machine][ori_pos-1], offspring[mu_machine][ori_pos]] \
        + s[mu_machine+1, offspring[mu_machine][ori_pos], offspring[mu_machine][ori_pos+1]] \
        + s[mu_machine+1, offspring[mu_machine][dest_pos-1], offspring[mu_machine][dest_pos]] \
        + s[mu_machine+1, offspring[mu_machine][dest_pos], offspring[mu_machine][dest_pos+1]] 
    
    if offsptime[mu_machine] > h[mu_machine+1]:
        offsbenefits[mu_machine] -= penalty * (offsptime[mu_machine] - h[mu_machine+1])
   
    return offspring, offsptime, offsbenefits

def outerMutation(offspring, offsptime, offsbenefits, Nmachines, s, p, b, h, penalty): 
    
    avail_machines = list(range(Nmachines))
    goto1 = True
    while goto1 == True:
        m_ori = random.choice(avail_machines)
        for i in range(len(offspring[m_ori])):
            if offspring[m_ori][i] == 0:
                m_ori_jobrange = i
                break
        if m_ori_jobrange == 0:
            goto1 = True
        else:
            goto1 = False
    
    j_ori = random.choice(list(range(m_ori_jobrange)))
    
    avail_machines = list(range(0, m_ori)) + list(range(m_ori+1, Nmachines))
    goto2 = True
    while goto2 == True:
        m_dest = random.choice(avail_machines)
        for i in range(len(offspring[m_dest])):
            if offspring[m_dest][i] == 0:
                m_dest_jobrange = i
                break
        if m_dest_jobrange == 0:
            goto2 = True
        else:
            goto2 = False
            
    j_dest = random.choice(list(range(m_dest_jobrange)))

    # update benefit
    offsbenefits[m_ori] = offsbenefits[m_ori] - b[m_ori+1, offspring[m_ori][j_ori]] + b[m_ori+1, offspring[m_dest][j_dest]]
    offsbenefits[m_dest] = offsbenefits[m_dest] - b[m_dest+1, offspring[m_dest][j_dest]] + b[m_dest+1, offspring[m_ori][j_ori]]

    # update ptime
    offsptime[m_ori] = offsptime[m_ori] \
    - s[m_ori+1, offspring[m_ori][j_ori-1], offspring[m_ori][j_ori]] \
    - s[m_ori+1, offspring[m_ori][j_ori], offspring[m_ori][j_ori+1]] \
    - p[m_ori+1, offspring[m_ori][j_ori]]
    
    offsptime[m_dest] = offsptime[m_dest] \
    - s[m_dest+1, offspring[m_dest][j_dest-1], offspring[m_dest][j_dest]] \
    - s[m_dest+1, offspring[m_dest][j_dest], offspring[m_dest][j_dest+1]] \
    - p[m_dest+1, offspring[m_dest][j_dest]]

    # update mutation of offspring1
    offspring[m_ori][j_ori], offspring[m_dest][j_dest] = \
    offspring[m_dest][j_dest], offspring[m_ori][j_ori]
    
    # update ptime
    offsptime[m_ori] = offsptime[m_ori] \
    + s[m_ori+1, offspring[m_ori][j_ori-1], offspring[m_ori][j_ori]] \
    + s[m_ori+1, offspring[m_ori][j_ori], offspring[m_ori][j_ori+1]] \
    + p[m_ori+1, offspring[m_ori][j_ori]]
    
    offsptime[m_dest] = offsptime[m_dest] \
    + s[m_dest+1, offspring[m_dest][j_dest-1], offspring[m_dest][j_dest]] \
    + s[m_dest+1, offspring[m_dest][j_dest], offspring[m_dest][j_dest+1]] \
    + p[m_dest+1, offspring[m_dest][j_dest]]

    if offsptime[m_ori] > h[m_ori+1]:
        offsbenefits[m_ori] -= penalty * (offsptime[m_ori] - h[m_ori+1])
    if offsptime[m_dest] > h[m_dest+1]:
        offsbenefits[m_dest] -= penalty * (offsptime[m_dest] - h[m_dest+1])
    
    return offspring, offsptime, offsbenefits


def readData(filepath):

    fo = open(filepath, "r")
    print ("file name", fo.name)
    lines = fo.readlines()
    fo.close()
    
    # machines, jobs
    Nmachines = 0
    Njobs = 0
    
    # parameter sets
    p = dict()
    s = dict()
    b = dict()
    h = dict()
    
    # handle read file
    for idx, line in enumerate(lines):
    	word = line.split(" ")
    
    	if word[0] == "param":
    		#line_id = idx+1
    		# machines
    		if word[1] == "I_num":
    			Nmachines = int(word[3])
    		# jobs
    		elif word[1] == "J_num":
    			Njobs = int(word[3])
    		# process time	
    		elif word[1] == "p:":
    			for counter in range(idx+1, idx+Nmachines+1):
    				p_line = lines[counter].split(" ")
    				I_index = p_line[0]
    				for J_index in range(0, Njobs+1):
    				    value = float(p_line[J_index+1])
    				    p[(int(I_index), int(J_index))] = value	
    
    		# benefit	
    		elif word[1] == "b:":
    			for counter in range(idx+1, idx+Nmachines+1):
    				b_line = lines[counter].split(" ")
    				I_index = b_line[0]
    				for J_index in range(0, Njobs+1):
    				    value = float(b_line[J_index+1])
    				    b[(int(I_index), int(J_index))] = value
    
    		# capacity
    		elif word[1] == "h":
    			for counter in range(idx+1, idx+Nmachines+1):
    				h_line = lines[counter].split(" ")
    				h[int(h_line[0])] = float(h_line[1])
    	# setup time	
    	elif word[0] == "*":
    		I_index = word[1]
    		for counter in range(idx+1, idx+1+Njobs+1):
    		    s_line = lines[counter].split(" ")
    		    J_index = s_line[0]
    		    for K_index in range(0, Njobs+1):
    		        value = float(s_line[K_index+1])
    		        s[(int(I_index), int(J_index),  int(K_index))] = value

    # print(Nmachines, Njobs)
    # print(p,"\n",s,"\n",b,"\n",h)
    return Nmachines, Njobs, p, s, b, h


## Parameters setting
Nmachines, Njobs, p, s, b, h = readData('C:/Users/user/Desktop/mythesis/testData/0000/0.txt')
Nindividuals = 100
Nloops = 3000
muMethod = 'outer' # 'inner', 'outer'
penalty = 1
crossMethod = 'MB' # 'MB', 'MI'
poolMethod = 'SR' # 'SR', 'TR'

cur_minb = 0
Nstop = 300
stop = 0
improve_loop = 0



## Generate initial solution pool 
individuals = np.zeros((1, Nmachines, Njobs))
ptimes = {}
benefits = {}
todo_jobs =[i for i in range(1, Njobs+1)]

if poolMethod == 'SR':
    Nindividuals -= 27

# Genearte initial pool randomly  
dd = 0
while dd < Nindividuals:
    
    indv = np.zeros((Nmachines, Njobs))
    ptime = [0 for i in range(Nmachines)]
    benefit = [0 for i in range(Nmachines)]
    
    # sort jobs randomly
    shuffle(todo_jobs) 
        
    for jcur in todo_jobs:
        # choose machine randomly
        find_m_assign = True
        while find_m_assign == True:
            m_assign = random.choice([i for i in range(Nmachines)]) 
            if len(np.where(indv[m_assign] == 0)[0]) != 0:
                find_m_assign = False
        # assign job randomly
        machine_length = np.where(indv[m_assign] == 0)[0][0]
        if machine_length == 0:
            insertpos = 0
        else:
            insertpos = random.choice([i for i in range(machine_length+1)])
            
        if insertpos == 0:
            ptime[m_assign] = ptime[m_assign] + p[m_assign+1, jcur] + s[m_assign+1, jcur, indv[m_assign][insertpos]]
        else:
            ptime[m_assign] = ptime[m_assign] + p[m_assign+1, jcur] + s[m_assign+1, jcur, indv[m_assign][insertpos]] \
            + s[m_assign+1, indv[m_assign][insertpos-1], jcur] - s[m_assign+1, indv[m_assign][insertpos-1], indv[m_assign][insertpos]]
            
            
        indv[m_assign] = np.insert(indv[m_assign][0:-1], insertpos, jcur)
        benefit[m_assign] += b[m_assign+1, jcur]

    for m in range(Nmachines):
        if ptime[m] > h[m+1]:
            benefit[m] -= penalty * (ptime[m] - h[m+1])
    
    dd+=1        
    individuals = np.append(individuals, [indv], axis = 0).reshape(dd+1, Nmachines, Njobs)
    ptimes[dd-1] = ptime
    benefits[dd-1] = benefit
  
individuals = np.delete(individuals, 0, axis=0)

if poolMethod == 'SR':
    # sort job by average, minimum, maximum benefit and CP value(benefit/processing time)
    avg_bf = {}
    min_bf = {}
    max_bf = {}
    avg_cp = {}
    min_cp = {}
    max_cp = {}
    for j in range(1, Njobs+1):
        sumb = 0
        sump = 0
        minb = 99999
        maxb = 0
        mincp = 99999
        maxcp = 0
        curcp = 0
        for i in range(1, Nmachines+1):
            sumb += b[i, j]
            sump += p[i, j]
            if p[i, j] == 0:
                curcp = b[i, j]
            else:
                curcp = b[i, j]/p[i, j]
            
            if curcp < mincp:
                mincp = curcp
            if curcp > maxcp:
                maxcp = curcp
            
            if b[i, j] < minb:
                minb = b[i, j]
            if b[i, j] > maxb:
                maxb = b[i, j]
            
        avg_bf[j] = sumb/Nmachines
        min_bf[j] = minb
        max_bf[j] = maxb
        if sump == 0:
            avg_cp[j] = sumb
        else:
            avg_cp[j] = sumb/sump
        min_cp[j] = mincp
        max_cp[j] = maxcp
        
    avg_bf_sorted = [job[0] for job in sorted(avg_bf.items(), key=lambda x:x[1], reverse = True)]
    min_bf_sorted = [job[0] for job in sorted(min_bf.items(), key=lambda x:x[1], reverse = True)]
    max_bf_sorted = [job[0] for job in sorted(max_bf.items(), key=lambda x:x[1], reverse = True)]
    avg_cp_sorted = [job[0] for job in sorted(avg_cp.items(), key=lambda x:x[1], reverse = True)]
    min_cp_sorted = [job[0] for job in sorted(min_cp.items(), key=lambda x:x[1], reverse = True)]
    max_cp_sorted = [job[0] for job in sorted(max_cp.items(), key=lambda x:x[1], reverse = True)]
    sortMethods = ('avgCP', 'minCP', 'maxCP', 'avgBF', 'minBF', 'maxBF', 'random')
    assignMethods = ('MBF', 'random')
    seqMethods = ('MI', 'random')
    poolOptions = []
    for sortMethod in sortMethods:
        for assignMethod in assignMethods:
            for seqMethod in seqMethods:
                option = (sortMethod, assignMethod, seqMethod)
                poolOptions.append(option)
    poolOptions.remove(('random', 'random', 'random'))
    
    # avg/min/max cp/benefit + MBF + MI
    option = 0
    for option in poolOptions:
        indv = np.zeros((Nmachines, Njobs))
        ptime = [0 for i in range(Nmachines)]
        benefit = [0 for i in range(Nmachines)]
        
        if option[0] == 'avgCP':
            todo_jobs = avg_cp_sorted.copy()
        elif option[0] == 'minCP':
            todo_jobs = min_cp_sorted.copy()
        elif option[0] == 'maxCP':
            todo_jobs = max_cp_sorted.copy()
        elif option[0] == 'avgBF':
            todo_jobs = avg_bf_sorted.copy()
        elif option[0] == 'minBF':
            todo_jobs = min_bf_sorted.copy()
        elif option[0] == 'maxBF':
            todo_jobs = max_bf_sorted.copy()
        elif option[0] == 'random':
            shuffle(todo_jobs)
            
        for jcur in todo_jobs:
            if option[1] == 'MBF':
                # choose machine with minimum benefit 
                m_assign = benefit.index(min(benefit))
            elif option[1] == 'random':
                # choose machine randomly
                find_m_assign = True
                while find_m_assign == True:
                    m_assign = random.choice([i for i in range(Nmachines)]) 
                    if len(np.where(indv[m_assign] == 0)[0]) != 0:
                        find_m_assign = False
            
            if option[2] == 'MI':
                # assign job to the minimum processing time after inserted
                curptime = 0
                bestptime = 99999
                bestpos = 0
                for k in range(Njobs):
                    if k == 0 and indv[m_assign][k] == 0:
                        bestptime = p[m_assign+1, jcur]
                        bestpos = 0
                        break
                    if k == 0:
                        curptime = ptime[m_assign] + p[m_assign+1, jcur] + s[m_assign+1, jcur, indv[m_assign][k]]
                    else:
                        curptime = ptime[m_assign] + p[m_assign+1, jcur] \
                        + s[m_assign+1, indv[m_assign][k-1], jcur] + s[m_assign+1, jcur, indv[m_assign][k]] \
                        - s[m_assign+1, indv[m_assign][k-1], indv[m_assign][k]]
                     
                    if curptime < bestptime:
                        bestptime = curptime
                        bestpos = k
                    
                    if k+1 >= Njobs:
                        break
                    else:
                        if indv[m_assign][k+1] == 0 and indv[m_assign][k] == 0:
                            break
                    
                indv[m_assign] = np.insert(indv[m_assign][0:-1], bestpos, jcur)
                ptime[m_assign] = bestptime
                benefit[m_assign] += b[m_assign+1, jcur]
            
            elif option[2] == 'random':
                # assign job randomly
                machine_length = np.where(indv[m_assign] == 0)[0][0]
                if machine_length == 0:
                    insertpos = 0
                else:
                    insertpos = random.choice([i for i in range(machine_length+1)])
                    
                if insertpos == 0:
                    ptime[m_assign] = ptime[m_assign] + p[m_assign+1, jcur] + s[m_assign+1, jcur, indv[m_assign][insertpos]]
                else:
                    ptime[m_assign] = ptime[m_assign] + p[m_assign+1, jcur] + s[m_assign+1, jcur, indv[m_assign][insertpos]] \
                    + s[m_assign+1, indv[m_assign][insertpos-1], jcur] - s[m_assign+1, indv[m_assign][insertpos-1], indv[m_assign][insertpos]]
                    
                    
                indv[m_assign] = np.insert(indv[m_assign][0:-1], insertpos, jcur)
                benefit[m_assign] += b[m_assign+1, jcur]
            
            
        for m in range(Nmachines):
            if ptime[m] > h[m+1]:
                benefit[m] -= penalty * (ptime[m] - h[m+1])
        
        Nindividuals += 1
        individuals = np.append(individuals, [indv], axis = 0).reshape(Nindividuals, Nmachines, Njobs)
        ptimes[Nindividuals-1] = ptime
        benefits[Nindividuals-1] = benefit

#print('---Initial Soltions---:\n', individuals, '\n indv nums:', len(individuals))
#print('pts:', ptimes, '\n bf:', benefits)  
        
# print('indv nums:', len(individuals))
maxminb1 = 0
opt_pick1 = 0 
for ind in range(Nindividuals):    
    curb1 = min(benefits[ind])
    if curb1 > maxminb1:
        maxminb1 = curb1
        opt_pick1 = ind
# print('initial pool optimal:', min(benefits[opt_pick1]))


for loop in range(Nloops):
    
    ## Selection
    # 抽一部份solutions，挑最小 benefit 最大的作為 parent，parent1 和 parent2 分別做   
    pick1 = pickparent(0.3, individuals, benefits, -1)
    parent1 = individuals[pick1]
    pick2 = pickparent(0.3, individuals, benefits, pick1)
    parent2 = individuals[pick2]
#    print('---Pick up parents---')
#    print('parent1:', parent1)
#    print('parent2:', parent2)
    

    ## Crossover
     
    offspring1 = np.zeros((Nmachines, Njobs))
    offspring2 = np.zeros((Nmachines, Njobs))
     
    # parent1 根據 cpoint 切成 offspring1, offspring2
    # random generate cpoints
    cpoints = []
    for i in range(Nmachines):
        for j in range(Njobs):
            if parent1[i][j] == 0:
                cpoints.append(random.randint(0, j))
                break            
#    print('cpoints:', cpoints)
        
    for i in range(Nmachines):
        offs1 = parent1[i][:cpoints[i]]
        offs2 = parent1[i][cpoints[i]:]
         
        for j in range(len(offs1)):
            offspring1[i][j] = offs1[j]
        for k in range(len(offs2)):
            offspring2[i][k] = offs2[k]
            
    offs1benefits = [] 
    offs2benefits = []  
    offs1ptime = []
    offs2ptime = []     
    for i in range(Nmachines):
        b1 = 0
        b2 = 0
        p1 = 0
        p2 = 0
        for j in range(Njobs):
            b1 += b[i+1, offspring1[i][j]]
            b2 += b[i+1, offspring2[i][j]]
            if j != 0:
                p1 += p[i+1, offspring1[i][j]] + s[i+1, offspring1[i][j-1], offspring1[i][j]]
                p2 += p[i+1, offspring2[i][j]] + s[i+1, offspring2[i][j-1], offspring2[i][j]]
            else:
                p1 += p[i+1, offspring1[i][j]] 
                p2 += p[i+1, offspring2[i][j]] 
       
        offs1benefits.append(b1)
        offs2benefits.append(b2)
        offs1ptime.append(p1)
        offs2ptime.append(p2)
        
#    print('---First seperate the parent 1 by cpoints---')
#    print('offspring 1: \n', offspring1)
#    print('offspring 2: \n', offspring2)
#    print('benefits of offspring 1:', offs1benefits, '\nbenefits of offspring 2:', offs2benefits)
#    print('ptime of offspring 1:', offs1ptime, '\nptime of offspring 2:', offs2ptime)
     
    
    ## MI Method：找同一台機器插入後 processing time 最小的位子 insert 
    if crossMethod == 'MI':
        # 將 parent2 裡還沒排進 offspring1 的工作排入 offspring1
        for i in range(Nmachines):
            for jcur in parent2[i]: 
                if jcur not in offspring1:
                    curptime = 0
                    bestptime = 99999
                    bestpos = 0
                    for k in range(Njobs):
    
                        if k == 0 and offspring1[i][k] == 0:
                            bestptime = p[i+1, jcur]
                            bestpos = 0
                            break
                        if k == 0:
                            curptime = offs1ptime[i] + p[i+1, jcur] + s[i+1, jcur, offspring1[i][k]]
                        else:
                            curptime = offs1ptime[i] + p[i+1, jcur] \
                            + s[i+1, offspring1[i][k-1], jcur] + s[i+1, jcur, offspring1[i][k]] \
                            - s[i+1, offspring1[i][k-1], offspring1[i][k]]
                         
                        if curptime < bestptime:
                            bestptime = curptime
                            bestpos = k
                        
                        if k+1 >= Njobs:
                            break
                        else:
                            if offspring1[i][k+1] == 0 and offspring1[i][k] == 0:
                                break
                        
                    offspring1[i] = np.insert(offspring1[i][0:-1], bestpos, jcur)
                    offs1ptime[i] = bestptime
                    if bestptime <= h[i+1]:            
                        offs1benefits[i] = offs1benefits[i] + b[i+1, jcur]
                    else:
                        offs1benefits[i] = offs1benefits[i] + b[i+1, jcur] - penalty * (bestptime - h[i+1])
                          
                else:
                    continue
                
        # 將 parent2 裡還沒排進 offspring2 的工作排入 offspring2
        for i in range(Nmachines):
            for jcur in parent2[i]: 
                if jcur not in offspring2:
                    curptime = 0
                    bestptime = 99999
                    bestpos = 0
                    for k in range(Njobs):
    
                        if k == 0 and offspring2[i][k] == 0:
                            bestptime = p[i+1, jcur]
                            bestpos = 0
                            break
                        if k == 0:
                            curptime = offs2ptime[i] + p[i+1, jcur] + s[i+1, jcur, offspring2[i][k]]
                        else:
                            curptime = offs2ptime[i] + p[i+1, jcur] \
                            + s[i+1, offspring2[i][k-1], jcur] + s[i+1, jcur, offspring2[i][k]] \
                            - s[i+1, offspring2[i][k-1], offspring2[i][k]]
                         
                        if curptime < bestptime:
                            bestptime = curptime
                            bestpos = k
     
                        if k+1 >= Njobs:
                            break
                        else:
                            if offspring2[i][k+1] == 0 and offspring2[i][k] == 0:
                                break
                        
                    offspring2[i] = np.insert(offspring2[i][0:-1], bestpos, jcur)
                    offs2ptime[i] = bestptime
                    if bestptime <= h[i+1]:            
                        offs2benefits[i] = offs2benefits[i] + b[i+1, jcur]
                    else:
                        offs2benefits[i] = offs2benefits[i] + b[i+1, jcur] - penalty * (bestptime - h[i+1])
                          
                else:
                    continue
            
  
    # MB Method：全面地看每台機器的每個位子，選 benefit 最小的機器 insert，並 insert 在插入後 processing time 最小的位子
    # 將 parent2 裡還沒排進 offspring1 的工作排入 offspring1
    elif crossMethod == 'MB':
        for i in range(Nmachines):
            for jcur in parent2[i]: 
                if jcur not in offspring1:
                    best_m = offs1benefits.index(min(offs1benefits))
                    curptime = 0
                    bestptime = 99999
                    bestpos = 0
                    for k in range(Njobs): 
                        if k == 0 and offspring1[best_m][k] == 0:
                            bestptime = p[best_m+1, jcur]
                            bestpos = 0
                            break
                        if k == 0:
                            curptime = offs1ptime[best_m] + p[best_m+1, jcur] + s[best_m+1, jcur, offspring1[best_m][k]]
                        else:
                            curptime = offs1ptime[best_m] + p[best_m+1, jcur] \
                            + s[i+1, offspring1[best_m][k-1], jcur] + s[best_m+1, jcur, offspring1[best_m][k]] \
                            - s[i+1, offspring1[best_m][k-1], offspring1[best_m][k]]
                        
                        if curptime < bestptime:
                            bestptime = curptime
                            bestpos = k
                            
                        if k+1 >= Njobs:
                            break
                        else:
                            if offspring1[best_m][k+1] == 0 and offspring1[best_m][k] == 0:
                                break
                        
                    offspring1[best_m] = np.insert(offspring1[best_m][0:-1], bestpos, jcur)
                    offs1ptime[best_m] = bestptime
                    if bestptime <= h[best_m+1]:            
                        offs1benefits[best_m] = offs1benefits[best_m] + b[best_m+1, jcur]
                    else:
                        offs1benefits[best_m] = offs1benefits[best_m] + b[best_m+1, jcur] - penalty * (bestptime - h[best_m+1])
                else:
                    continue

        # 將 parent2 裡還沒排進 offspring1 的工作排入 offspring2
        for i in range(Nmachines):
            for jcur in parent2[i]: 
                if jcur not in offspring2:
                    best_m = offs2benefits.index(min(offs2benefits))
                    curptime = 0
                    bestptime = 99999
                    bestpos = 0
                    for k in range(Njobs): 
                        if k == 0 and offspring2[best_m][k] == 0:
                            bestptime = p[best_m+1, jcur]
                            bestpos = 0
                            break
                        if k == 0:
                            curptime = offs2ptime[best_m] + p[best_m+1, jcur] + s[best_m+1, jcur, offspring2[best_m][k]]
                        else:
                            curptime = offs2ptime[best_m] + p[best_m+1, jcur] \
                            + s[i+1, offspring2[best_m][k-1], jcur] + s[best_m+1, jcur, offspring2[best_m][k]] \
                            - s[i+1, offspring2[best_m][k-1], offspring2[best_m][k]]
                        
                        if curptime < bestptime:
                            bestptime = curptime
                            bestpos = k
                            
                        if k+1 >= Njobs:
                            break
                        else:
                            if offspring2[best_m][k+1] == 0 and offspring2[best_m][k] == 0:
                                break
                        
                    offspring2[best_m] = np.insert(offspring2[best_m][0:-1], bestpos, jcur)
                    offs2ptime[best_m] = bestptime
                    if bestptime <= h[best_m+1]:            
                        offs2benefits[best_m] = offs2benefits[best_m] + b[best_m+1, jcur]
                    else:
                        offs2benefits[best_m] = offs2benefits[best_m] + b[best_m+1, jcur] - penalty * (bestptime - h[best_m+1])
                else:
                    continue
 
#    print('---After crossover----')
#    print('offs1: \n', offspring1)
#    print('offs2: \n', offspring2)  
#    print('benefits of offspring 1:', offs1benefits, '\nbenefits of offspring 2:', offs2benefits)
#    print('ptime of offspring 1:', offs1ptime, '\nptime of offspring 2:', offs2ptime)

    ## Mutation
    # Inter mutation: 隨機選一機器、隨機二工作交換
    # Outer mutation: 隨機選二機器、隨機教換其中工作
    # 兩個子代分別有機率發生 mutation
    
    Pmu = 3
    
    r1 = random.randint(1, 10)
    r2 = random.randint(1, 10)

    if r1 <= Pmu:
        if muMethod == 'outer':
            offspring1, offs1ptime, offs1benefits = outerMutation(offspring1, offs1ptime, offs1benefits, Nmachines, s, p, b, h, penalty)
        else:
            offspring1, offs1ptime, offs1benefits = shiftMutation(offspring1, offs1ptime, offs1benefits, Nmachines, s, h, penalty)
    
    if r2 <= Pmu:  
        if muMethod == 'outer':
            offspring2, offs2ptime, offs2benefits = outerMutation(offspring2, offs2ptime, offs2benefits, Nmachines, s, p, b, h, penalty)
        else:
            offspring2, offs2ptime, offs2benefits = shiftMutation(offspring2, offs2ptime, offs2benefits, Nmachines, s, h, penalty)

    
    ## Update solution pool: 丟掉最差的 0/1/2 個 solution，加入新的 0/1/2 個 solution
    # 拿掉 pool 裡最差，並加入新的兩個子代
        

    minbenefit = 99999
    pick = 0 # 挑選一組最差的solution拿掉
    for ind in range(Nindividuals):    
        curb = min(benefits[ind])
        if curb < minbenefit:
            minbenefit = curb
            pick = ind
    if minbenefit < min(offs1benefits):
        # update pool ,benefits and ptime 
        individuals = np.delete(individuals, pick, axis = 0)
        individuals = np.insert(individuals, pick, [offspring1], axis = 0)
        benefits[pick] = offs1benefits
        ptimes[pick] = offs1ptime           

    minbenefit = 99999
    pick = 0 # 挑選一組最差的solution拿掉
    for ind in range(Nindividuals):    
        curb = min(benefits[ind])
        if curb < minbenefit:
            minbenefit = curb
            pick = ind
    if minbenefit < min(offs2benefits):
        # update pool ,benefits and ptime
        individuals = np.delete(individuals, pick, axis = 0)
        individuals = np.insert(individuals, pick, [offspring2], axis = 0)
        benefits[pick] = offs2benefits
        ptimes[pick] = offs2ptime
        
        
    maxminb1 = 0
    opt_pick1 = 0 
    for ind in range(Nindividuals):    
        curb1 = min(benefits[ind])
        if curb1 > maxminb1:
            maxminb1 = curb1
            opt_pick1 = ind
            
    objectives.append(min(benefits[opt_pick1]))
    
    if min(benefits[opt_pick1]) > cur_minb:
        cur_minb = min(benefits[opt_pick1])
        improve_loop = loop+1
        stop = 0
    else:
        stop += 1
    
    if stop >= Nstop:
        print('stop loop times:', loop+1)
        break
    
#    print('LoopEnd opt benefits:', benefits[opt_pick1])
    



# ---  After GA --- ##
# Optimal solution: 抓出 pool 裡最好的解

maxminb = 0
opt_pick = 0 
for ind in range(Nindividuals):    
    curb = min(benefits[ind])
    if curb > maxminb:
        maxminb = curb
        opt_pick = ind

final_solution = individuals[opt_pick]

print('---final solution---\n', final_solution)

#z_opt, time_opt = mp.MILPmodel(Nmachines, Njobs, p, s, b, h)
#z_opts = [z_opt for i in range(Nloops+1)]
# loops = [i for i in range(loop+2)]

# plt.plot(loops, objectives)
#plt.plot(loops, z_opts)
print('last improve loop:', improve_loop)
## Output: gantt chart

#tmplist = []
#machinetiming = [0 for i in range(Nmachines)]
#for i in range(Nmachines):
#    curtime = 0
#    prev = 0
#    for jcur in final_solution[i]:
#        
#        starttime = machinetiming[i]
#        setuptime = s[i+1, prev, jcur]
#        processingtime = p[i+1, jcur]
#        finishtime = starttime + setuptime + processingtime
#        tmplist.append(dict(Task = "Machine "+str(i+1), Start = convert_to_datetime(starttime + setuptime),\
#                       Finish = convert_to_datetime(finishtime)))
#        prev = jcur
#        machinetiming[i] = finishtime
#        
#        if jcur == 0:
#            break
#
#df_result = pd.DataFrame(tmplist)
#
#num_tick_labels = np.linspace(start = 0, stop = max(machinetiming), num = max(machinetiming)+1, dtype = int)
#date_ticks = [convert_to_datetime(x) for x in num_tick_labels]
#
#
#fig = ff.create_gantt(df_result, group_tasks=True, showgrid_x=True, showgrid_y=True, index_col='Task')
#
#
#fig.layout.update(
#        autosize = True,
#        xaxis = {
#        'tickmode' : 'array',
#        'tickvals' : date_ticks,
#        'ticktext' : num_tick_labels,
#        'automargin': True
#        })
#
#
#fig.write_html('GA_benefit_figure1.html', auto_open=False)
#
#
print('min benefits:', min(benefits[opt_pick]), '\nptimes:', ptimes[opt_pick], '\nloops:', Nloops)

