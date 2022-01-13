#!/usr/bin/env python
# coding: utf-8
# thsu0407@gamil.com


import numpy as np
import pandas as pd
def get_ener(path1 = "./OSZICAR"):
    """
    only for H cac
    """
    f=open(path1,'r+')
    flist=f.readlines()
    totener = float(flist[-1].strip().split()[4])

    return totener
def get_pv(path1 = "./OUTCAR"):
    f=open(path1,'r+')
    flist=f.readlines()
    external = []
    volume = []
    for i in flist:
        if "external" in i :
            external.append(i)
            #pass
        elif "volume" in i :
            #print(i)
            volume.append(i)
    p = external[-1].split()[3]
    v = volume[-1].split()[4]
    print("p:",p,"v",v)
    return p,v
def sca_pos(sca,path = "POSCAR"):
    import sys,os
    sca = sca
    f=open(path,'r+')
    flist=f.readlines()
    flist[1]=str(sca) + '\n'
    f=open(path,'w+')
    f.writelines(flist)
    return sca
def submit(i):
    import os
    import time
    import os.path
    import time
    import re
    os.mkdir("./sca"+str(i))                                           ###创建关于缩放因子名称的文件夹
    os.system("cp -r demo/* ./sca"+str(i))                             ###把除了POSCAR之外的文件都拷贝到创建的文件夹里
    os.system("wait")
    os.system("cp POSCAR ./sca"+str(i))                                ### 把上一步的POSCAR拷过来，一定是上一步的
    sca_pos(i,path = "./sca"+str(i)+"/POSCAR")                         ###根据i值（缩放因子），修改POSCAR
    #os.system("cp para.txt ./sca"+str(i))
    os.system("wait")
    ##############################  文件准备结束  ############################
    time.sleep(1)
    mine = os.getcwd()
    os.chdir(str(mine)+"/sca"+str(i))
    os.system("bsub < yxq.lsf")  ## rw and submit vasp task
    os.chdir(str(mine))
    os.system("mv POSCAR old_POSCAR")
    scf = 0

    while abs(scf)<1:
        if os.path.isfile("./sca"+str(i)+"/02_scf/already_scf"):
            print("scf ending...")
            scf = 1
            data_path  = "./sca"+str(i)+"/02_scf/"
            ener = get_ener(path1=data_path+"OSZICAR")
            p,v = get_pv(path1=data_path+"OUTCAR")
            H = float(ener) + (float(p)*float(v)/1600)
            #para = [i,ener,p,v,H]
            #np.savetxt(str(i)+'_para.txt',para,fmt='%s')

            os.chdir(data_path)
            os.system("cp POSCAR ../../")
            os.chdir(str(mine))

    return float(i),float(ener),float(p),float(v),H
	
	
   
#df = pd.DataFrame()
Slist = []
Elist = []
Plist = []
Vlist = []
Hlist = []    
    
flag = 0
scaling = 1
while flag < 1:
    scaling = round(scaling - 0.001,5)
    i,ener,p,v,H = submit(i=scaling)
    if float(p) > 1000:
        flag = 1
    else:
        flag = 0
        if scaling > 0:
            Slist.append(i)
            Elist.append(ener)
            Plist.append(p)
            Vlist.append(v)
            Hlist.append(H)
            df = pd.DataFrame()
            df["Sca"] = Slist
            df["Ener"] = Elist
            df["P"] = Plist
            df["v"] = Vlist
            df["H"] = Hlist
            df.to_csv("./data.csv",index=None)
