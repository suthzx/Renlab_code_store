#!/usr/bin/env python
# coding: utf-8

# In[10]:


import spglib
import random
import re

"""
input total number and positions,numbers means the diff elems type
"""
# elem_total = 4
# positions = [[0.3, 0.3, 0.0],[0.5, 0.53, 0.0],[0.0, 0.5, 0.5],[0.5, 0.0, 0.5]] # Ni
# numbers = [1, 1, 1, 2]  
# a_b_c = int(elem_total**0.333)

def cif_local(path="./test_gen_basis_24.cif"):
    """
    read cif get Local_pos(Tensor)
    """
    with open (path) as f:
        flag = 0
        sourceInLine=f.readlines()
    flag = 0
    local = []
    for i in sourceInLine:

        if "_atom_site_occupancy" in i:
            flag = 1
        if flag == 0:
            pass
        elif flag ==1:
            #print(i)
            local.append(i)
    Local_pos = []
    for i in range(1,len(local)-1):
        local_pos = []
        x1 = local[i].split()[3] 
        x2 = local[i].split()[4]
        x3 = local[i].split()[5]
        local_pos.append(float(x1))
        local_pos.append(float(x2))
        local_pos.append(float(x3))
        Local_pos.append(local_pos)
    return Local_pos
def refine_mat(positions,numbers,a_b_c):
    spg = []
    lat = []
    for _ in range(100):
        positions = positions
        numbers = numbers       # 与type有关
        try:
            cell_mat = [] 
            for x in range(10):
                cell_mat.append(random.uniform(1.4,a_b_c))
            lattice = [[cell_mat[0], cell_mat[1], cell_mat[2]],
                       [cell_mat[3], cell_mat[4], cell_mat[5]],
                       [cell_mat[6], cell_mat[7], cell_mat[8]]]
            
            cell = (lattice, positions, numbers)
            symmetry_refine = spglib.refine_cell(cell, symprec=1e-1)
            print(symmetry_refine)
            symmetry = spglib.get_spacegroup(symmetry_refine, symprec=1e-1)
            spgnumber = str(symmetry)
            print(spgnumber)
            kk = re.compile(r'\d+')
            result = re.findall(kk,spgnumber)[-1]
            spg.append(result)
            lat.append(symmetry_refine)
            print(result)
            print("-----------------------------------------")
        except:
            print("False")
            print("-----------------------------------------")
            pass
    return spg,lat


# In[12]:


elem_total = len(cif_local())
positions = cif_local()
numbers = [1, 1, 1, 2]  
a_b_c = int(elem_total**0.333)
a,b = refine_mat(positions=positions,numbers=numbers,a_b_c=a_b_c)


# In[ ]:




