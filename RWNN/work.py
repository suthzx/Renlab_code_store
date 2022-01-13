#coding:utf-8
#thsu0407@gmail.com
import time
import os
import os.path
import numpy as np
import pandas as pd
sblist = [] ## some-break-samble
enerlist = []
idlist = []
search = range(101,120)
def get_ener_peer(path1,path2):
#path1 = "./OSZICAR"
    with open(path1,  "r", encoding='utf-8') as f:
        lines = f.readlines()
        line_1 = lines[-1].split()
        E0 = line_1[4]
        E0 = float(E0)
#path2 = "./POSCAR"
    with open(path2,  "r", encoding='utf-8') as f:
        N = []
        lines = f.readlines()
        line_7 = lines[6].split()
        N = [ float(n) for n in line_7 ]
        N_all = sum(N)
    E = E0 / N_all
    return E

for i in search:
    os.system("cp demo ./rw_"+str(i)+" -r")
    os.system("wait")
    os.system("cp CONTCAR ./rw_"+str(i))
    os.system("wait")
    print("go to "+str(i)+" times random walk optimize search")
    time.sleep(1)
    mine = os.getcwd()
    os.chdir(str(mine)+"/rw_"+str(i))
    os.system("bash ./goRW.sh")
    os.chdir(str(mine))
    scf = 0
    while abs(scf)<1:
        if os.path.isfile("./rw_"+str(i)+"/02_scf/already_scf"):
            print("scf ending...")
            scf = 1


for i in search:
    try:
        ener = np.float(get_ener_peer(path1="./rw_"+str(i)+"/02_scf/OSZICAR",path2="./rw_"+str(i)+"/02_scf/POSCAR"))
        print(ener)
        idlist.append(i)
        enerlist.append(ener)
    except:
        sblist.append(i)
print(idlist)
print(enerlist)
print(sblist)

data = pd.DataFrame()
data["id"]=idlist
data["ener"]=enerlist
print(data)
data.to_csv("./ener&id",index=None)
