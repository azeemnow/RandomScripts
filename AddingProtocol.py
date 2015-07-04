import csv
file = open("FormattedDomains.csv", "w")

domains = open('top500domains.csv', 'r')
domainsReader = csv.reader(domains)

domains = ["https://www." + row[1] for row in domainsReader]
for domain in domains:
   file.write(domain + "\n")

file.close()
#Thanks (@azeemnow)
