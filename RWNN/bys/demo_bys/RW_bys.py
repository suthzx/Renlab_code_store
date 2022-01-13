#coding:utf-8
#thsu0407@gmail.com
import numpy as np 
import random 
import os 
path = "./CONTCAR"
topath = "./RWCS_test"
import os
try:
    os.makedirs(topath)
except:
    print("already done")
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
            
            
########################################################################
#para = [[1,20,10000,1,1,1,1,1],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1]]  ##para shap as input
para = np.loadtxt('para.txt').tolist()
########################################################################
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
cova = []
_ = pos("./CONTCAR",type="opt",para=para)
for i in _.lst_atyp:
    #print(i,elem_cova[str(i)]/100)
    cova.append(elem_cova[str(i)]/100)
cova.sort()
rw_req = cova[0]+cova[1]
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
   # if rw_min > 0:         #### get it pass!
    flag = 1
    _.output("./POSCAR")
    _.output(topath+"/POSCAR")
