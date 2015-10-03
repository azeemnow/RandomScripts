import socket

#create an empty list
ListOfHostNames = []

#open a csv file named "hostnames" that contains list of hostnames.
#Use line.strip to remove whitespaces
#Populates the data into the empty list
with open('hostnames.csv', 'r') as f:
    for line in f:
        line = line.strip()
        ListOfHostNames.append(line)

#open "hostname.csv" as a new file in write mode
newFile = open('hostnames.csv', 'w')
print(ListOfHostNames)

#create a for loop to run each hostname in the ListOfHostNames list and runs it aginst the socket.gethostbyname module
for name in ListOfHostNames:
    try:
        ResolveHostname = socket.gethostbyname(name)
        print(ResolveHostname)

#write results out to the newFile in each newline
        newFile.write(ResolveHostname + "\n")
        print(ResolveHostname)

#for any hostnames that could not get resolved - two exceptions are created.
#the result of the exception is written to the newFile including the exception name and the applicable hostname
    except (socket.herror, socket.gaierror) as e:
        #newFile.write("No resolution available for %s" % (name) + "\n")
        newFile.write("No resolution available for %s: %s" % (name, e) + "\n")
newFile.close()
