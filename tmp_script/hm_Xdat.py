DATA = []
XDAT = []
fileHandler  =  open  ("./XDATCAR",  "r")
while  True:
    # Get next line from file
    line  =  fileHandler.readline()
    # If line is empty then end of file reached
    if  not  line  :
        break;
    #print(line.strip())
    XDAT.append(line.strip())
    # Close Close 
    #fileHandler.close()
f=open("XDAT.txt","a")
for i in range(0,4999):  ####考虑清楚到底是多少个
    f.write("{}\n".format(str(XDAT[2+(i*332)])))
f.close()