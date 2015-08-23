import socket

ListOfIPAddresses = []

with open('top500ips.csv', 'r') as f: #top500ips.csv is a sample file. You can add your own file name
    for line in f:
        line = line.strip()
        ListOfIPAddresses.append(line)

newFile = open('top500ips.csv', 'w') #top500ips.csv is the same file I opened above; I am replacing the original file. You can give it a different name  

for address in ListOfIPAddresses:
    try:
        ResolvedAddress = socket.gethostbyaddr(address)[0]
        newFile.write(ResolvedAddress + "\n")
        # print(ResolvedAddresses)
    except socket.herror as e:
        newFile.write("No resolution available for %s" % (address) + "\n")
newFile.close()

