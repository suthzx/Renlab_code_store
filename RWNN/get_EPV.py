#!/usr/bin/env python
# coding: utf-8
# thsu0407@gamil.com


def get_ener(path1 = "./OSZICAR"):
    """
    only for H cac
    """
    f=open(path1,'r+')
    flist=f.readlines()
    totener = float(flist[-1].strip().split()[4])
    print(totener)
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


get_ener()
get_pv()

