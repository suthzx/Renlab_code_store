data = []
fileHandler  =  open  ("./OUTCAR",  "r")
while  True:
    # Get next line from file
    line  =  fileHandler.readline()
    # If line is empty then end of file reached
    if  not  line  :
        break;
    #print(line.strip())
    data.append(line.strip())
    # Close Close 
    #fileHandler.close()
for i in data:
    if "NBANDS" in i:
        #print(i)
        tar = str(i)
nba = int(tar.split()[-1])

for i in [".DIAG",".GW0",".NONE",".BSE"]
    fp=open("INCAR"+str(i),"a",encoding="utf-8")
    fp.write("\nNBANDS = "+str(nba))
    fp.close()
