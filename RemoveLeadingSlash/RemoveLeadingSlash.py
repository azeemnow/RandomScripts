import csv

domains = open('domainlist.csv', 'r')
DomainListCSV = csv.reader(domains)
DomainList = [column[1] for column in DomainListCSV]
StripList = [item.rstrip('/') for item in DomainList]
print('\n'.join(StripList))

