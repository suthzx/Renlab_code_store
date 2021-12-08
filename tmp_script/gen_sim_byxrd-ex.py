#!/usr/bin/env python
# coding: utf-8


import time
import os
import queue
import threading
from multiprocessing.dummy import Pool as ThreadPool
from pyxtal import pyxtal
from pyxtal.XRD import Similarity
import pandas as pd
#import re
def dif_ex(a,b,t):
    """
    imput a and b (both list type)
    imput T as the dif controls parameter 
    return result via the 1 and 0 
    """
    import math
    result = None
    T = t   #temperature 
    value_sum = 0 
    a = list(map(lambda x: x ** 2, list(a[1])))
    b = list(map(lambda x: x ** 2, list(b[1])))
    for i in range(len(a)):
        numerator = abs(a[i] - b[i]) * -1    
        denominator = a[i]
        x = (abs(denominator)*-1)/(denominator*T)
        value = math.exp(x)
        value_sum = value_sum + value
    if value < 0.1:
        result = 0
    else:
        result = 1
    return result
def test_th(th):
    """
    th = threshold
    Test the structural index and number of threshold (temperature) releases
    """
    j_list = []
    for i in [1]:
            for j in range(1,5000):
                xtal1 = pyxtal()
                xtal2 = pyxtal()
                xtal1.from_seed(my_dir+"/"+str(i)+'.cif')
                xtal2.from_seed(my_dir+"/"+str(j)+'.cif')
                xrd1 = xtal1.get_XRD(thetas=[0, 180])
                xrd2 = xtal2.get_XRD(thetas=[0, 180])
                p1 = xrd1.get_profile()
                p2 = xrd2.get_profile()
                test = dif_ex(p1,p2,th)   ## import the th
                print(i,j)
                print(test,"dif_ex")
                if test == 0:
                    j_list.append(j)
                print("-------------------------------------------")
    print(th,len(j_list))
    file_handle=open(str(th)+'_'+str(len(j_list))+'.txt',mode='w')
    file_handle.write(str(th)+'_'+str(len(j_list))+' \n')
    return j_list

#for i in range(5000):
#    my_crystal = pyxtal()
#    my_crystal.from_random(3, 160, ['Ba','Ti','O'], [3,3,9])
#    #my_crystal.show(supercell=(2,2,2))
#    #my_crystal.to_ase().write("./rand_str/"+str(i)+'.vasp', forma t='vasp', vasp5=True)
#    my_crystal.to_file("./sim/"+str(i)+'.cif')
# In[2]:


my_dir = "/share/home/sutianhao/gangtie/hzw/SS/RW_['Hf', 'O']/spnb_2_cell/102"

#my_dir = "/share/home/sutianhao/gangtie/hzw/SS/sim"



if __name__ == '__main__':
    print("I am ",os.cpu_count(),"cores CPU")  
    inex = []
    scor = []
    th_list = [0.001,0.005,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]
    pool = ThreadPool(12) 
    pool.map(test_th, th_list) 
    pool.close()
    pool.join()
