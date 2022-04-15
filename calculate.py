import os
import pandas as pd

path = 'C:/Users/user/Desktop/mythesis/'

fileList = []
for root, dirs, files in os.walk(path+'merge_TimeEfficiency_pool50'):
  for file in files:
    fileList.append(file)

performanceFile = open('avgPerformace_over30_pool50.csv', "w", encoding = 'utf-8')
performanceFile.write('scenario, avg_TR-OM-Inner, avg_TR-OM-Outer, avg_TR-LB-Inner, avg_TR-LB-Outer, \
avg_SR-OM-Inner, avg_SR-OM-Outer, avg_SR-LB-Inner, avg_SR-LB-Outer, \
min_TR-OM-Inner, min_TR-OM-Outer, min_TR-LB-Inner, min_TR-LB-Outer, \
min_SR-OM-Inner, min_SR-OM-Outer, min_SR-LB-Inner, min_SR-LB-Outer, \
time_opt, time_TR-OM-Inner, time_TR-OM-Outer, time_TR-LB-Inner, time_TR-LB-Outer, \
time_SR-OM-Inner, time_SR-OM-Outer, time_SR-LB-Inner, time_SR-LB-Outer, \
std_TR-OM-Inner, std_TR-OM-Outer, std_TR-LB-Inner, std_TR-LB-Outer, \
std_SR-OM-Inner, std_SR-OM-Outer, std_SR-LB-Inner, std_SR-LB-Outer,\
Loop_TR-OM-Inner, Loop_TR-OM-Outer, Loop_TR-LB-Inner, Loop_TR-LB-Outer,\
Loop_SR-OM-Inner, Loop_SR-OM-Outer, Loop_SR-LB-Inner, Loop_SR-LB-Outer, \
Loop_std_TR-OM-Inner, Loop_std_TR-OM-Outer, Loop_std_TR-LB-Inner, Loop_std_TR-LB-Outer,\
Loop_std_SR-OM-Inner, Loop_std_SR-OM-Outer, Loop_std_SR-LB-Inner, Loop_std_SR-LB-Outer')

# performanceFile.write('filename, (avgCP-MBF-MI), (avgCP-MBF-random), (avgCP-random-MI), (avgCP-andom-random), (minCP-MBF-MI), (minCP-MBF-random), \
#     (minCP-random-MI), (minCP-random-random), (maxCP-MBF-MI), (maxCP-MBF-random), (maxCP-random-MI), (maxCP-random-random), \
#     (avgBF-MBF-MI), (avgBF-MBF-random), (avgBF-random-MI), (avgBF-random-random), (minBF-MBF-MI), (minBF-MBF-random), (minBF-random-MI), \
#     (minBF-random-random), (maxBF-MBF-MI), (maxBF-MBF-random), (maxBF-random-MI), (maxBF-random-random), (random-MBF-MI), (random-MBF-random), \
#     (random-random-MI)')
performanceFile.write('\n')

col_names = ['filename', 'z_opt', 'z_ga', 'z_ga2', 'z_ga3', 'z_ga4', 'z_ga5', 'z_ga6', 'z_ga7', 'z_ga8', \
'time_opt', 'time_ga', 'time_ga2', 'time_ga3', 'time_ga4', 'time_ga5', 'time_ga6', 'time_ga7', 'time_ga8', \
'improveLoop', 'improveLoop2', 'improveLoop3', 'improveLoop4', 'improveLoop5', 'improveLoop6', 'improveLoop7', \
'improveLoop8']

for filename in fileList:
  filepath = path + 'merge_TimeEfficiency_pool50/' + filename
  df = pd.read_csv(filepath, names = col_names, header = 0, encoding = 'utf-8')
  df['pf_1'] = df['z_ga']/df['z_opt']
  df['pf_2'] = df['z_ga2']/df['z_opt']
  df['pf_3'] = df['z_ga3']/df['z_opt']
  df['pf_4'] = df['z_ga4']/df['z_opt']
  df['pf_5'] = df['z_ga5']/df['z_opt']
  df['pf_6'] = df['z_ga6']/df['z_opt']
  df['pf_7'] = df['z_ga7']/df['z_opt']
  df['pf_8'] = df['z_ga8']/df['z_opt']

  print(filename)

  performanceFile.write(str(filename) + ',' + str(round(df['pf_1'].mean(),3)) + ',' + str(round(df['pf_2'].mean(),3))+ ',' \
  + str(round(df['pf_3'].mean(),3)) + ',' + str(round(df['pf_4'].mean(),3)) + ',' \
  + str(round(df['pf_5'].mean(),3)) + ',' + str(round(df['pf_6'].mean(),3))+ ',' \
  + str(round(df['pf_7'].mean(),3)) + ',' + str(round(df['pf_8'].mean(),3)) + ',' \
  + str(round(df['pf_1'].min(),3)) + ',' + str(round(df['pf_2'].min(),3))+ ',' \
  + str(round(df['pf_3'].min(),3)) + ',' + str(round(df['pf_4'].min(),3)) + ',' \
  + str(round(df['pf_5'].min(),3)) + ',' + str(round(df['pf_6'].min(),3))+ ',' \
  + str(round(df['pf_7'].min(),3)) + ',' + str(round(df['pf_8'].min(),3)) + ',' \
  + str(round(df['time_opt'].mean(),3)) + ','+ str(round(df['time_ga'].mean(),3)) + ',' \
  + str(round(df['time_ga2'].mean(),3)) + ',' + str(round(df['time_ga3'].mean(),3)) + ',' \
  + str(round(df['time_ga4'].mean(),3)) + ','+ str(round(df['time_ga5'].mean(),3)) + ',' \
  + str(round(df['time_ga6'].mean(),3)) + ',' + str(round(df['time_ga7'].mean(),3)) + ',' \
  + str(round(df['time_ga8'].mean(),3)) + ',' + str(round(df['pf_1'].std(),3)) + ',' \
  + str(round(df['pf_2'].std(),3))+ ',' + str(round(df['pf_3'].std(),3)) + ',' \
  + str(round(df['pf_4'].std(),3)) + ',' + str(round(df['pf_5'].std(),3)) + ',' \
  + str(round(df['pf_6'].std(),3))+ ',' + str(round(df['pf_7'].std(),3)) + ',' \
  + str(round(df['pf_8'].std(),3)) + ',' + str(round(df['improveLoop'].mean(),3)) + ',' \
  + str(round(df['improveLoop2'].mean(),3)) + ',' + str(round(df['improveLoop3'].mean(),3)) + ',' \
  + str(round(df['improveLoop4'].mean(),3))+ ',' + str(round(df['improveLoop5'].mean(),3)) + ',' \
  + str(round(df['improveLoop6'].mean(),3)) + ',' + str(round(df['improveLoop7'].mean(),3)) + ',' \
  + str(round(df['improveLoop8'].mean(),3)) + ',' + str(round(df['improveLoop'].std(),3)) + ',' \
  + str(round(df['improveLoop2'].std(),3)) + ',' + str(round(df['improveLoop3'].std(),3)) + ',' \
  + str(round(df['improveLoop4'].std(),3))+ ',' + str(round(df['improveLoop5'].std(),3)) + ',' \
  + str(round(df['improveLoop6'].std(),3)) + ',' + str(round(df['improveLoop7'].std(),3)) + ',' \
  + str(round(df['improveLoop8'].std(),3)))
  performanceFile.write('\n')
   
performanceFile.close()


# # merge results
# fileList = []
# for root, dirs, files in os.walk(path+'result_lp_TimeEfficiency'):
#    for file in files:
#        fileList.append(file)

# # col_names1 = ['filename', 'z_opt', 'time_opt']
# # col_names2 = ['filename', 'TR-MI-Inter', 'TR-MI-Outer', 'TR-MB-Inter', 'TR-MB-Outer', 'SR-MI-Inter', 'SR-MI-Outer', \
#     # 'SR-MB-Inter', 'SR-MB-Outer', 'time_TR-MI-Inter', 'time_TR-MI-Outer', 'time_TR-MB-Inter', 'time_TR-MB-Outer', \
#     # 'time_SR-MI-Inter', 'time_SR-MI-Outer', 'time_SR-MB-Inter', 'time_SR-MB-Outer', \
#     # 'Loop_TR-MI-Inter', 'Loop_TR-MI-Outer', 'Loop_TR-MB-Inter', 'Loop_TR-MB-Outer', \
#     # 'Loop_SR-MI-Inter', 'Loop_SR-MI-Outer', 'Loop_SR-MB-Inter', 'Loop_SR-MB-Outer']


# for file in fileList:
# 	filepath1 = path + 'result_lp_TimeEfficiency/' + file
# 	df1 = pd.read_csv(filepath1, header = 0, encoding = 'utf-8')
# 	filepath2 = path + 'result_ga_TimeEfficiency_pool50/' + file
# 	df2 = pd.read_csv(filepath2, header = 0, encoding = 'utf-8')

# 	df2.insert(1, 'z_opt', df1[' z_opt'])
# 	df2.insert(10, 'time_opt', df1[' time_opt'])
# 	# merged = df1.merge(df2, on = 'filename')
# 	df2.to_csv(path + 'merge_TimeEfficiency_pool50/'+ file, sep = ',', index = False, encoding = 'utf-8')
# 	