import csv

#open csv file with list of domain in read only
domains = open('domainlist.csv', 'r')
#pull only the second column from the csv file while using csv.reader module
DomainList = [column[1] for column in csv.reader(domains)]
#use strip to remove the right /
StripList = [item.rstrip('/') for item in DomainList]
#print the output on each new line
print('\n'.join(StripList))

