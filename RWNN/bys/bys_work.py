#!/usr/bin/env python
# coding: utf-8

import time
import optuna
import numpy as np
import pandas as pd
search = []
enerlist = []
idlist = []
bklist = []


elem_cova = {'H': 31.0,'He': 28.0,'Li': 128.0, 'Be': 96.0, 'B': 84.0, 'C': 76.0, 'N': 71.0, 'O': 66.0, 'F': 57.0, 'Ne': 58.0, 'Na': 166.0,
         'Mg': 141.0, 'Al': 121.0, 'Si': 111.0, 'P': 107.0, 'S': 105.0, 'Cl': 102.0, 'Ar': 106.0, 'K': 203.0, 'Ca': 176.0,'Sc': 170.0, 
         'Ti': 160.0,'V': 153.0, 'Cr': 139.0, 'Mn': 139.0, 'Fe': 132.0, 'Co': 126.0, 'Ni': 124.0, 'Cu': 132.0, 'Zn': 122.0, 'Ga': 122.0, 
         'Ge': 120.0, 'As': 119.0, 'Se': 120.0, 'Br': 120.0, 'Kr': 116.0, 'Rb': 220.0, 'Sr': 195.0, 'Y': 190.0, 'Zr': 175.0, 
         'Nb': 164.0, 'Mo': 154.0, 'Tc': 147.0, 'Ru': 146.0, 'Rh': 142.0, 'Pd': 139.0, 'Ag': 145.0, 'Cd': 144.0, 'In': 142.0, 
         'Sn': 139.0, 'Sb': 139.0, 'Te': 138.0, 'I': 139.0, 'Xe': 140.0, 'Cs': 244.0, 'Ba': 215.0, 'La': 207.0, 'Ce': 204.0, 
         'Pr': 203.0, 'Nd': 201.0, 'Pm': 199.0, 'Sm': 198.0, 'Eu': 198.0, 'Gd': 196.0, 'Tb': 194.0, 'Dy': 192.0, 'Ho': 192.0,
         'Er': 189.0, 'Tm': 190.0, 'Yb': 187.0, 'Lu': 187.0, 'Hf': 175.0, 'Ta': 170.0, 'W': 162.0, 'Re': 151.0, 'Os': 144.0,
         'Ir': 141.0, 'Pt': 136.0, 'Au': 136.0, 'Hg': 132.0, 'Tl': 145.0, 'Pb': 146.0, 'Bi': 148.0,'Po': 140.0, 'At': 150.0, 
         'Rn': 150.0, 'Fr': 260.0, 'Ra': 221.0, 'Ac': 215.0, 'Th': 206.0, 'Pa': 200.0, 'U': 196.0, 'Np': 190.0, 'Pu': 187.0,
         'Am': 180.0, 'Cm': 169.0}


class pos:
    def __init__(self, fname="./POSCAR",type="auto",para=None):
        self.raw_data = [iline.strip().split() for iline in open(fname,'r').read().strip().split("\n")]
        self.mat_cell = np.array(self.raw_data[2:5], dtype=float)
        self.mat_frac = float(self.raw_data[1][0])
        self.mat_cell = self.mat_frac*self.mat_cell
        self.inv_cell = np.linalg.inv(self.mat_cell)
        self.lst_atom = np.array(self.raw_data[6],dtype=int)
        self.tot_atom = np.sum(self.lst_atom) 
        self.lst_atyp = self.raw_data[5] 
        self.loc_atom = np.array(self.raw_data[8:8+self.tot_atom],dtype=float)
        if "D" in self.raw_data[7][0]:
            self.frc_cord = self.loc_atom.copy()
            self.loc_atom = np.matmul(self.frc_cord, self.mat_cell) 
        else :
            self.frc_cord = np.matmul(self.loc_atom, self.inv_cell)

        if type =="auto":
            self.max_step = 1.0 ##1.0 å
        elif type=="opt":
            self.max_step = para  ##opt param space
    def mutation(self):
        tmv = np.random.RandomState().normal(scale=self.max_step,size=(self.tot_atom,3))
        self.loc_atom = self.loc_atom + tmv 
        self.frc_cord = np.matmul(self.loc_atom, self.inv_cell)
    def opt_mutation(self):
        tmv = []
        print(self.max_step)
        for x in range(self.tot_atom):     
            #print(self.max_step[0][x])
            tmr = self.max_step[0][x]  ## para = [para_r,para_s,para_p]
            phi = self.max_step[1][x]
            sei = self.max_step[2][x]
            #print(tmr)
            tmx = float(tmr*np.sin(phi)*np.cos(sei))
            tmy = float(tmr*np.sin(phi)*np.sin(sei))
            tmz = float(tmr*np.cos(phi))
            tms = [tmx,tmy,tmz]
            #print(x,tms)
            #print("-"*6)
            tmv.append(tms)
        self.loc_atom = self.loc_atom + tmv 
        self.frc_cord = np.matmul(self.loc_atom, self.inv_cell)
    def output(self, oname="./POSCAR"):
        with open(oname, 'w') as f:
            print(self.raw_data[0][0],file=f)
            print("1.00000",file=f)
            [print("  {0[0]:16.12f}  {0[1]:16.12f}  {0[2]:16.12f}".format(i), file=f) for i in self.mat_cell]
            print(" ".join(self.lst_atyp),file=f)
            print(" ".join(["{}".format(ia) for ia in self.lst_atom]),file=f)
            print("Direct", file=f)
            print("\n".join(["  {0[0]:16.12f}  {0[1]:16.12f}  {0[2]:16.12f}".format(i) for i in self.frc_cord]), file=f)

def get_ener_peer(path1,path2):
    with open(path1, "r", encoding='utf-8') as f:
        lines = f.readlines()
        line_1 = lines[-1].split()
        E0 = line_1[4]
        E0 = float(E0)
    with open(path2, "r", encoding='utf-8') as f:
        N = []
        lines = f.readlines()
        line_7 = lines[6].split()
        N = [ float(n) for n in line_7 ]
        N_all = sum(N)
    E = E0 / N_all
    return E
def hist(search):   
    search = search
    for i in search:
        try:
            ener = np.float(get_ener_peer(path1="./rw_bys"+str(i)+"/02_scf/OSZICAR",path2="./rw_"+str(i)+"/02_scf/POSCAR"))
            print(ener)
            idlist.append(i)
            enerlist.append(ener)
        except:
            bklist.append(i)
    print(idlist)
    print(enerlist)
    print(bklist)
    #import pandas as pd
    data = pd.DataFrame()
    data["id"]=idlist
    data["ener"]=enerlist
    print(data)
    return data.to_csv("./ener&id",index=None)
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
    
def atm_unmber(path="./CONTCAR"):
    atm = 0
    for i in find_formula(path)[0]:
        atm+=1
    return atm

def force( path1 = "./OUTCAR",path2 = "./POSCAR"):
    import numpy as np
    path1 = path1
    path2 = path2
    mark = None
    DAT = []
    cell_atom_num = 0
    line_num = 0
    fileHandler = open(path1,"r")
    while  True:
        line  =  fileHandler.readline()
        if  not  line  :
            break;
        DAT.append(line)
    print("DAT",DAT)
    for r in DAT:
        #print(r)  
        if "total drift:" in r:
            mark = line_num
        else:
            pass
        line_num += 1
    print("mark",mark)
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
    print(int(cac_force*10000))
    return cac_force*10000

def submit(i):
    import os
    import time
    import os.path
    import time
    import re
    os.mkdir("./rw_bys"+str(i))
    os.system("cp -r demo_bys/* ./rw_bys"+str(i))
    os.system("wait")
    os.system("cp CONTCAR ./rw_bys"+str(i))
    os.system("cp para.txt ./rw_bys"+str(i))
    os.system("wait")
    print("go to "+str(i)+" times random walk optimize search")
    time.sleep(1)
    mine = os.getcwd()
    os.chdir(str(mine)+"/rw_bys"+str(i))
    os.system("bash ./goRW.sh")  ## rw and submit vasp task
    os.chdir(str(mine))
    scf = 0
    while abs(scf)<1:
        if os.path.isfile("./rw_bys"+str(i)+"/02_scf/already_scf"):
            print("scf ending...")
            scf = 1
            ener = np.float64(get_ener_peer(path1="./rw_bys"+str(i)+"/02_scf/OSZICAR",path2="./rw_bys"+str(i)+"/02_scf/POSCAR"))
            Force = force(path1="./rw_bys"+str(i)+"/02_scf/OUTCAR",path2="./rw_bys"+str(i)+"/02_scf/POSCAR")
            print(i,ener)
            print(i,Force)
            #search.append(i)
    #np.savetxt("search_index",search)
    #print(search)
    return Force
def gen_para(para = [[1,2,3,4,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]):
    import numpy as np
    para = para
    np.savetxt('para.txt',para)


def objective(trial):
    import time
    atm1_r = trial.suggest_float("atm1_r", 0.3, 1.2)
    atm2_r = trial.suggest_float("atm2_r", 0.3, 1.2)
    atm3_r = trial.suggest_float("atm3_r", 0.3, 1.2)
    atm4_r = trial.suggest_float("atm4_r", 0.3, 1.2)
    atm5_r = trial.suggest_float("atm5_r", 0.3, 1.2)
    atm6_r = trial.suggest_float("atm6_r", 0.3, 1.2)
    atm7_r = trial.suggest_float("atm7_r", 0.3, 1.2)
    atm8_r = trial.suggest_float("atm8_r", 0.3, 1.2)
    
    atm1_s = trial.suggest_float("atm1_s", 0, 360)
    atm2_s = trial.suggest_float("atm2_s", 0, 360)
    atm3_s = trial.suggest_float("atm3_s", 0, 360)
    atm4_s = trial.suggest_float("atm4_s", 0, 360)
    atm5_s = trial.suggest_float("atm5_s", 0, 360)
    atm6_s = trial.suggest_float("atm6_s", 0, 360)
    atm7_s = trial.suggest_float("atm7_s", 0, 360)
    atm8_s = trial.suggest_float("atm8_s", 0, 360)
    
    atm1_p = trial.suggest_float("atm1_p", 0, 360)
    atm2_p = trial.suggest_float("atm2_p", 0, 360)
    atm3_p = trial.suggest_float("atm3_p", 0, 360)
    atm4_p = trial.suggest_float("atm4_p", 0, 360)
    atm5_p = trial.suggest_float("atm5_p", 0, 360)
    atm6_p = trial.suggest_float("atm6_p", 0, 360)
    atm7_p = trial.suggest_float("atm7_p", 0, 360)
    atm8_p = trial.suggest_float("atm8_p", 0, 360)
    
    para = [[atm1_r,atm2_r,atm3_r,atm4_r,atm5_r,atm6_r,atm7_r,atm8_r],
            [atm1_s,atm2_s,atm3_s,atm4_s,atm5_s,atm6_s,atm7_s,atm8_s],
            [atm1_p,atm2_p,atm3_p,atm4_p,atm5_p,atm6_p,atm7_p,atm8_p]]
    
    gen_para(para=para)
    cova = []
    _ = pos("./CONTCAR",type="opt",para=para)
    for i in _.lst_atyp:
        #print(i,elem_cova[str(i)]/100)
        cova.append(elem_cova[str(i)]/100)  #change it to å
    cova.sort()
    rw_req = cova[0]+cova[1]  # Threshold element
    flag = 0
    rw_req = rw_req
    s = 0
    while flag == 0:
        _ = pos("./CONTCAR",type="opt",para=para)
        _.opt_mutation()
        rw_loc = _.loc_atom
        rw_dis = []
        for i in range(len(rw_loc)-1):
            for j in range(i):
                rw_distance = (rw_loc[i][0] - rw_loc[i+1][0])**2 + (rw_loc[i][1]-rw_loc[i+1][1])**2 + (rw_loc[i][2]-rw_loc[i+1][2])**2
                #print("a,b:",i,j,rw_distance)
                rw_dis.append(rw_distance)
        rw_min = min(rw_dis)
        s = s+1
        print("test_",s)
        if rw_min > 0:    ### get it all  pass !
            flag = 1
            #_.output("./POSCAR")
            #_.output(topath+"/POSCAR")
            tm= str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).replace(" ", "-").replace(":","").replace("-","")
            FForce = submit(i=tm)
            gold = float(FForce)
        else:
            #tm= str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())).replace(" ", "-").replace(":","").replace("-","")
            FForce = 99999
            pass

    return FForce

study = optuna.create_study()
study.optimize(objective, n_trials=300)





