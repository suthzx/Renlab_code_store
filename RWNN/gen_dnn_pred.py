#coding:utf-8
#thsu0407@gmail.com
import os
import time
import pandas as pd
import numpy as np
import tensorflow as tf
from pyxtal import pyxtal
from pymatgen.core.structure import Structure
from megnet.models import MEGNetModel
from megnet.data.crystal import CrystalGraph
from megnet.utils.preprocessing import StandardScaler
INTENSIVE = False 
class xtb:
    def __init__(self):
        from ase import Atoms
        from ase.io import read, write
        from ase.optimize import BFGS
        from ase.io.trajectory import Trajectory
        from xtb.ase.calculator import XTB
        os.environ['XTBHOME'] = "/share/home/sutianhao/anaconda3/envs/pyxtal"
        os.environ['XTBPATH'] = "/share/home/sutianhao/anaconda3/envs/pyxtal/share/xtb"
        os.environ['PATH'] = "/share/home/sutianhao/anaconda3/envs/pyxtal/bin:{}".format(os.environ['PATH'])
        self.water =read(cifpath)
        self.BFGS = BFGS
    def xtb_opt(cifpath='BaTiO3_mp-5777_computed.cif',optpath='out.vasp'):
        water.calc = XTB(method = "GFN0-xTB")
        opt = BFGS(water, trajectory = 'opt.traj')
        opt.run(fmax = 0.1)
        # traj = Trajectory('opt.traj')
        # for atoms in traj:
        #      print(atoms.positions, atoms.get_potential_energy())
        write(optpath, water)

class gen_cif:
    def __init__(self,dim,elemlist,per,sup_scale):
        self.space = []
        self.dim = dim
        self.elemlist = elemlist
        self.per = per
        self.sup_scale = sup_scale
        self.pyxtal = pyxtal()
        self.fescore = []
        self.spnb = []
        self.t0 = time.time()
        self.t1 = time.time()
        self.cif_path = None
        self.structure = None
        self.model = None
    def find_spg(self): 
        space = self.space
        for i in range(1,231):
            try:
                my_crystal = self.pyxtal
                my_crystal.from_random(dim,i,elemlist,per)           
                space.append(i)
            except:          
                pass
        return space

    def run_gen(self):
        t0 = self.t0
        for sup in sup_scale:
            perlist = [ i*sup for i in per]  ## 元素比例
            sp = gen_cif.find_spg(self)
            for i in sp :
                import os
                try:
                    os.makedirs("./RW_"+str(elemlist)+"/spnb_"+str(sup)+"_cell/"+str(i))
                except:
                    print("already done")  
                for t in range(1,5000):
                    from pyxtal import pyxtal
                    my_crystal = pyxtal()
                    my_crystal.from_random(dim, i, elemlist, perlist)
                    #my_crystal.show(supercell=(2,2,2))
                    #my_crystal.to_ase().write("./rand_str/"+str(i)+'.vasp', forma t='vasp', vasp5=True)
                    my_crystal.to_file("./RW_"+str(elemlist)+"/spnb_"+str(sup)+"_cell/"+str(i)+"/"+str(t)+'.cif')
                    if t%1000 ==0:
                        print("./RW_"+str(elemlist)+"/spnb_"+str(sup)+"_cell/"+str(i)+"/"+str(t)+'.cif_gen_')
            print(sup,"cell done") 
        t1=self.t1
        print("Time：%.6fs"%(t1-t0))   
        return sp

    def cif2structure(cif_path):
        """get cif to ase.Structure"""
        cif_path = cif_path
        return Structure.from_file(cif_path)

    def get_structure_hidden_vector_from_model(self):
        """some times may use it"""
        structure = self.structure
        model = self.model
        graph = model.graph_converter.convert(structure)
        inp = model_form.graph_converter.graph_to_input(graph)
        sub_model = tf.keras.models.Model( inputs = model.input, outputs = model.get_layer('dense_19').output)
        return sub_model(inp)

    def run_pred(self):  
        prd_model = MEGNetModel.from_file('formation_energy.hdf5')
        gbest = pd.DataFrame()
        t0=time.time()
        for sup in sup_scale:
            perlist = [ i*sup for i in per]
            sp = gen_cif.find_spg(self)
            try:
                os.makedirs("./RW_"+str(elemlist)+"/ML_select")
            except:
                print("already done")  
            for i in sp :
                gopath = "./RW_"+str(elemlist)+"/spnb_"+str(sup)+"_cell/"
                sub_score = pd.DataFrame()
                fescore = []
                pathdir = []
                for z in range(1,5000):
                    structure = gen_cif.cif2structure(gopath+str(i)+"/"+str(z)+".cif")
                    pred_fe = prd_model.predict_structure(structure)
                    fescore.append(pred_fe)
                    pathdir.append(gopath+str(i)+"/"+str(z)+".cif")
                sub_score["dir"] = pathdir
                sub_score["pred_fe"] = np.array(fescore)
                sub_score.sort_values(by="pred_fe" , inplace=True, ascending=True) 
                p_best = sub_score[:1]
                print(p_best)
                gbest = gbest.append(p_best)

        t1=time.time()
        gbest.to_csv("./RW_"+str(elemlist)+"/ML_select"+"/ML_index_select.csv",index=None)
        print("Time：%.6fs"%(t1-t0))



#############################################################################  
dim = 3                #Crystal dimension
elemlist = ['Zn','Mg','O']   #Elements in crystals
per = [3,1,4]            #Ratio of elements: point to point from elemlist(The smallest scale was set to 1)
sup_scale = [1,2]  #Multiples of elements in a unit cell

############################################################################# 
if __name__ == '__main__':

    x = gen_cif(dim = dim,elemlist = elemlist,per = per,sup_scale = sup_scale)
    x.run_gen()
    #x.run_pred()









