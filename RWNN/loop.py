#coding:utf-8
#thsu0407@gmail.com
##loop.py
import numpy as np
def find_formula(path = "./BaTiO3_mp-5777_computed.vasp"):
    box = []
    with open(path, "r") as f:
        file = f.readlines()
        box.append(file)
    symbol = box[0][5].strip().split()
    number = box[0][6].strip().split()
    formula = str()
    for i in range(len(symbol)):
        #print(i)
        #print(symbol[i],number[i])
        formula = formula+symbol[i]+number[i]
    return formula,number

path1 = "./OUTCAR"
path2 = "./POSCAR"
DAT = []
cell_atom_num = 0
line_num = 0
fileHandler  =  open(path1,"r")
while  True:
    line  =  fileHandler.readline()
    if  not  line  :
        break;
    DAT.append(line)
for r in DAT:
    #print(r)  
    if "total drift:" in r:
        mark = line_num
        #print(line_num)
    else:
        pass
    line_num += 1
a,b = find_formula(path2)
for i in b:
    cell_atom_num+=int(i)
Drift = DAT[mark-cell_atom_num-2:mark+1]

force_sum = []
for force in [x.split()[3:] for x in Drift[1:-2]]:
    force_sum.append(force[0])
    force_sum.append(force[1])
    force_sum.append(force[2])
cac_force = abs(np.float32(force_sum)).max()
print(cac_force)
