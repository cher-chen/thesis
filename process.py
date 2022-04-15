import os
import pandas as pd
import model_milp as m
import model_ga as g

# =============================================================================
# Call functions:
# MILPmodel(Nmachines, Njobs, p, s, b, h)
# GAmodel(Nmachines, Njobs, p, s, b, h, poolMethod, sortMethod, muMethod)
# =============================================================================

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


    return Nmachines, Njobs, p, s, b, h



dir_list = []
path = 'C:/Users/user/Desktop/mythesis/'
for root, dirs, files in os.walk(path+'testData_remain_prev'):
    for dir in dirs:
        dir_list.append(dir)

if not(os.path.exists(path + 'result')):
    os.mkdir(path + 'result')

recordFile = open(path + 'record.txt', 'w', encoding = 'utf-8')

for dir in dir_list:
    if dir != '2001':
        continue
    resultFilename = path +'result/' + str(dir) + '.csv'
    resultFile = open(resultFilename, "w", encoding = 'utf-8')
    resultFile.write('filename, z_opt, z_ga, z_ga2, z_ga3, z_ga4, time_opt, time_ga, time_ga2, time_ga3, time_ga4, \
    improveLoop, improveLoop2, improveLoop3, improveLoop4')
    resultFile.write('\n')
    for root, dirs, files in os.walk(path + 'testData_remain_prev/' + str(dir)):
        for file in files:
            filepath = path + 'testData_remain_prev/' + str(dir) + '/' + file
            recordFile.write(filepath+'\n')
            Nmachines, Njobs, p, s, b, h = readData(filepath)
            z_opt, time_opt = m.MILPmodel(Nmachines, Njobs, p, s, b, h)
            ## GAmodel(Nmachines, Njobs, p, s, b, h, poolMethod, crossMethod, muMethod)
            z_ga, time_ga, improve_loop = g.GAmodel(Nmachines, Njobs, p, s, b, h, 'TR', 'MI', 'inter')
            z_ga2, time_ga2, improve_loop2 = g.GAmodel(Nmachines, Njobs, p, s, b, h, 'TR', 'MI', 'outer')
            z_ga3, time_ga3, improve_loop3 = g.GAmodel(Nmachines, Njobs, p, s, b, h, 'TR', 'MB', 'inter')
            z_ga4, time_ga4, improve_loop4 = g.GAmodel(Nmachines, Njobs, p, s, b, h, 'TR', 'MB', 'outer')
            # z_ga, time_ga, improve_loop = g.GAmodel(Nmachines, Njobs, p, s, b, h, 'SR', 'MI', 'inter')
            # z_ga2, time_ga2, improve_loop2 = g.GAmodel(Nmachines, Njobs, p, s, b, h, 'SR', 'MI', 'outer')
            # z_ga3, time_ga3, improve_loop3 = g.GAmodel(Nmachines, Njobs, p, s, b, h, 'SR', 'MB', 'inter')
            # z_ga4, time_ga4, improve_loop4 = g.GAmodel(Nmachines, Njobs, p, s, b, h, 'SR', 'MB', 'outer')
 
            resultFile.write(str(file) + ',' + str(z_opt) + ',' + str(z_ga) + ',' + str(z_ga2) + ',' \
                             + str(z_ga3) + ',' + str(z_ga4) + ',' + str(time_opt) + ',' + str(time_ga) + ',' \
                             + str(time_ga2) + ','+ str(time_ga3) + ','+ str(time_ga4) + ',' \
                             + str(improve_loop) + ',' + str(improve_loop2) + ',' + str(improve_loop3) + ',' \
                             + str(improve_loop4))
            resultFile.write('\n')
            
    resultFile.close()


 
#fileList = []
#for root, dirs, files in os.walk(path+'result'):
#    for file in files:
#        fileList.append(file)
#
#performanceFile = open('avgPerformace.csv', "w", encoding = 'utf-8')
#performanceFile.write('scenario, pf_1, pf_2, pf_, pf_3, time_opt, time_1, time_2, time_3, time_4')
#performanceFile.write('\n')
#
#col_names = ['filename', 'z_opt', 'z_ga', 'z_ga2', 'z_ga3', 'z_ga4', 'time_opt', 'time_ga', 'time_ga2', 'time_ga3', 'time_ga4']
#
#for filename in fileList:
#    filepath = path + 'result/' + filename
#    df = pd.read_csv(filepath, names = col_names, header = 0, encoding = 'utf-8')
#    df['pf_1'] = df['z_ga']/df['z_opt']
#    df['pf_2'] = df['z_ga2']/df['z_opt']
#    df['pf_3'] = df['z_ga3']/df['z_opt']
#    df['pf_4'] = df['z_ga4']/df['z_opt']
#
#    print(filename)
#
#    performanceFile.write(str(filename) + ',' + str(round(df['pf_1'].mean(),3)) + ',' + str(round(df['pf_2'].mean(),3))+ ',' \
#                          + str(round(df['pf_3'].mean(),3)) + ',' + str(round(df['pf_4'].mean(),3)) + ',' \
#                          + str(round(df['time_opt'].mean(),3)) + ','+ str(round(df['time_ga'].mean(),3)) + ',' \
#                          + str(round(df['time_ga2'].mean(),3)) + ',' + str(round(df['time_ga3'].mean(),3)) + ',' \
#                          + str(round(df['time_ga4'].mean(),3)))
#    performanceFile.write('\n')
#    
#    
#    
#
#performanceFile.close()
