import numpy as np
import os
import random


# ==============================================
# size n/m : ["small 5", "mid 10", "big 20"]
# setuptime/process time propotion : [0.5, 1, 2]
# capacity : ["tight","loose"]
# sequence-independent setup time : ["no","yes"]
# ==============================================

instance_num = 20

def create(s, a, c, w, num):
    datafile = open("testData/large_15/"+str(s)+str(a)+str(c)+str(w)+"/"+str(num)+".txt", "w")

    # size
    m = random.randint(2, 5)
    if s == 2:
        n = m * 15 
    elif s == 4:
        n = m * 40
    else:
        n = m * 50

    print("param I_num :=", m, ";\nparam J_num :=", n, ";", file = datafile)	

    # benefit
    print("param b:", end = " ", file = datafile)
    for j in range(n+1):
        print(j, end = " ", file = datafile)
    print(":=", end = "\n", file = datafile)
    for i in range(1, m+1):
        print(i, end = " ", file = datafile)
        for j in range(n+1):
            if j == 0:
                temp_b = 0
            else:
                temp_b = round(np.random.uniform(low = 0, high = 20))
                # temp_b = round(np.random.normal(loc = 10, scale = 5.0), 3)
                # while temp_b < 0:
                #     temp_b = round(np.random.normal(loc = 10, scale = 5.0), 3) 
            print(temp_b, end = " ", file = datafile)
        print("", end="\n", file = datafile)
    print(";", file = datafile)

    process_time = {}
    setup_time = {}
    if a == 0:
        time_factor = 0.5
    elif a == 1:
        time_factor = 1
    else:
        time_factor = 2

    # setup times
    for i in range(1, m+1):
        for j in range(n+1):
            total_s = 0
            temp_sj = round(np.random.uniform(low = 0, high = 10))
            # temp_sj = round(np.random.normal(loc = 5, scale = 2.5), 3)
            # while temp_sj < 0:
            #     temp_sj = round(np.random.normal(loc = 5, scale = 2.5), 3)
            for k in range(n+1):
                if j == 0 or k == 0 or j == k:
                    setup_time[(i, j, k)] = 0
                else:
                    temp_sjk = round(np.random.uniform(low = 0, high = 10))
                    # temp_sjk = round(np.random.normal(loc = 5, scale = 2.5), 3)
                    # while temp_sjk < 0:
                    #     temp_sjk = round(np.random.normal(loc = 5, scale = 2.5), 3)
                    if w == 0: # sequence-dependent setup time
                        setup_time[(i, j, k)] = temp_sjk
                    else: # sequence-independent setup time
                        setup_time[(i, j, k)] = temp_sj
                    total_s += setup_time[(i, j, k)]
                    
    avg_setup_time = sum(setup_time.values()) / (n * n * m)
    
    avg_ptime = avg_setup_time / time_factor
    for i in range(1, m + 1):
        for j in range(n + 1):  
            if j == 0:
                process_time[(i, j)] = 0
            else:
                process_time[(i, j)] = round(np.random.uniform(low = 0, high = avg_ptime * 2))

          
#            ptime = (total_s/n)/time_factor
#
#            if j == 0:
#                process_time[(i, j)] = 0
#            else:
#                process_time[(i, j)] = round(ptime, 3)
                

    # processing time
    print("param p:", end = " ", file = datafile)
    for j in range(n+1):
        print(j, end = " ", file = datafile)
    print(":=", end = "\n", file = datafile)
    for i in range(1, m+1):
        print(i, end = " ", file = datafile)
        for j in range(n+1):
            temp_p = process_time[i, j]
            print(temp_p, end = " ", file = datafile)
        print("", end="\n", file = datafile)

    print(";", file = datafile)


    # setup time
    print("param s:= ", end = "\n", file = datafile)

    for i in range(1, m+1):
        print("*",i,":", end = " ", file = datafile)
        for w in range(n+1):
            print(w, end = " ", file = datafile)
        print (":= ", end = "\n", file = datafile)
        for j in range(n+1):
            print(j, end = " ", file = datafile)
            for k in range(n+1):
                print(setup_time[i,j,k], end = " ", file = datafile)
            print("", end="\n", file = datafile)


    print(";", end = "\n", file = datafile)


    if c == 0: # tight
        capacity_factor = 0.75
    elif c == 1: # loose
        capacity_factor = 1
    else: # very loose
        capacity_factor = 1.25

    miu = (sum(setup_time.values()) / (n*m) + sum(process_time.values()) / m) / m
    
    capacity = miu * capacity_factor

    # capacity
    print("param h := ", end = "\n", file = datafile)
    for i in range(1, m+1):
        # capacity = np.random.normal(loc = capacity_factor * miu, scale = capacity_factor * miu * 0.5)
        # while capacity < 0:
        #     capacity = np.random.normal(loc = capacity_factor * miu, scale = capacity_factor * miu * 0.5)
        print(i, round(capacity, 3), end = "\n", file = datafile)

    print(";", file = datafile)


def main():

    for s in range(2, 3): # size 
        for a in range(3): # average setuptime/process time
            for c in range(3): # capacity
                for w in range(2): # sequence-dependent setup time
                    print(s, a, c, w)
                    if not(os.path.exists("testData/large_15")):
                        os.mkdir("testData/large_15")
                    if not(os.path.exists("testData/large_15/"+str(s)+str(a)+str(c)+str(w))):
                        os.mkdir("testData/large_15/"+str(s)+str(a)+str(c)+str(w))
                    for num in range(instance_num):
                        create(s, a, c, w, num)


if __name__ == "__main__":
	main()