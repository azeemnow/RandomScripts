#***This script looks-up values from one CSV file against the second master CSV file and prints result.***

f1 = csv.reader(open('ext_master.csv', 'r')) #first csv file
master = {} #declare a dictionary
for row in f1:
    master[row[0]] = row[1:]
    #create a dic with the first column as the key & rest as values


f2 = csv.reader(open('new_ext.csv', 'r')) #second csv file
for row in f2:
    if row[0] in master:
        print(row + master[row[0]])
       # print the interate row from f2 & matching values from the master dic
    if row[0] not in master:
        print('not in master list:  ' + (row[0]))
        #msg string plus interate row from f2
        
#Thanks --azeemnow        
