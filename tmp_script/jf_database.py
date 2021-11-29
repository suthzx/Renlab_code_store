import pandas as pd
import numpy as np
import os
import time
import ase.io
def native_cp(str_log_open,str_new):
    import os
    import shutil
    str_log_open = str_log_open 
    shutil.copyfile(str_log_open, str_new)
try:
    os.mkdir("./id_file")
    print("creat")
except:
    os.system("rm id_file -r")
    os.mkdir("./id_file")
    print("re-creat")
    
def sin_feature(path1): 
    with open(path1,  "r", encoding='utf-8') as f:
            lines = f.readlines() 
    feature_sin = list()        
    for i in [-1,-2,-3]:
        for j in [0,1,2]:
            #print(lines[i].split()[j])
            feature_sin.append(lines[i].split()[j])
    feature_sin = pd.DataFrame(feature_sin).T
    return feature_sin
def ener_per(path1,path2):
    with open(path1,  "r", encoding='utf-8') as f:
        lines = f.readlines() 
        line_1 = lines[-1].split()
        E0 = line_1[4]
        E0 = float(E0)  
    with open(path2,  "r", encoding='utf-8') as f:
        N = []
        lines = f.readlines() 
        line_7 = lines[6].split()
        N = [ float(n) for n in line_7 ]
        N_all = sum(N)
    E = E0 / N_all
    return E
filelist = os.listdir(os.getcwd())
done_index = []
for i in filelist:
    if "jf_" in i:
        #print(i)
        done_index.append(i)
#done_index
#path1="/public/home/tianhaosu/My_work/jf/"+str(t)+"/POSCAR"
#path2="/public/home/tianhaosu/My_work/jf/"+str(t)+"/OSZICAR"
enerlist = []
index  = []
des = pd.DataFrame()
for t in done_index:
    try:  
        
        ener = ener_per(path1="./"+str(t)+"/OSZICAR",
                        path2="./"+str(t)+"/POSCAR")
        enerlist.append(ener)
        des  = des.append(sin_feature(path1="./"+str(t)+"/POSCAR" ))
        tmp = ase.io.read("./"+str(t)+"/POSCAR")
        tmp.write("./"+str(t)+"/"+str(t)+".cif")
        native_cp("./"+str(t)+"/"+str(t)+".cif","./id_file/"+str(t)+".cif")
        index.append(t)
    except:
        print("that index sth wrong","*****",str(t))
des["index"] = index
des["Y"] = enerlist
des.to_csv("./origin.csv",index=None)