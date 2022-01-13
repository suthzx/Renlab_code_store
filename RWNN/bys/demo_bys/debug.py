### 生成首先随机行走的集合
import numpy as np
import random
import sys,os
path = "./CONTCAR"
topath = "./RWCS_test"
import os
try:
    os.makedirs(topath)
except:
    print("already done")  
TMP = []
box = []
with open(path, "r") as f:
    file = f.readlines()
    box.append(file)
    #symbol = box[0][5].strip().split()
latt = max(box[0][2].strip().split()+box[0][3].strip().split()+box[0][4].strip().split())
number = box[0][6].strip().split()
cac = 0
for i in number:
    cac = cac +int(i)
for i in range(1000):
    tmp = []
    for i in range(3):
        data =  random.uniform(-1,1)     ### 标注
        tmp.append(data)
    if  0.0001<tmp[0]**2 + tmp[1]**2 + tmp[2]**2  < (1/float(latt)) :     ### 标注
        #print(tmp)
        #print(tmp[0]**2 + tmp[1]**2 + tmp[2]**2)
        TMP.append(tmp)
        #break
    else:
        pass

f=open(path,'r+')
flist=f.readlines()
#print(flist)
for i in range(cac):
    x_origin = float(box[0][8+i].strip().split()[0])
    y_origin = float(box[0][8+i].strip().split()[1])
    z_origin = float(box[0][8+i].strip().split()[2])
    r = int(random.uniform(0,len(TMP)))
    #print(r)
    x_random = x_origin + TMP[r][0]
    y_random = y_origin + TMP[r][1]
    z_random = z_origin + TMP[r][2]
    replace = str(x_random)+"\t"+str(y_random)+"\t"+str(z_random)+'\n'
    flist[8+i]=replace
    f=open("./POSCAR",'w+')
    f.writelines(flist)
    f.close()