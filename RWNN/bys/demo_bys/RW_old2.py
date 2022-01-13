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
	def __init__(self, fname="./POSCAR"):
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
		self.max_step = 1.0 ##1.0 å
	
	def mutation(self):
		tmv = np.random.RandomState().normal(scale=self.max_step,size=(self.tot_atom,3))
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

_ = pos("./CONTCAR")
_.mutation() 
_.output("./POSCAR")
