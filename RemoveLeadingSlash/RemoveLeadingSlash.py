import csv
DomainList = []

domains = open('domainlist.csv', 'r')
DomainList = csv.reader(domains)
DomainList = [column[1] for column in DomainList]
strip_list = [item.rstrip('/') for item in DomainList]
print('\n'.join(strip_list))


