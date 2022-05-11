#!/usr/bin/env python
# coding: utf-8



def read_loopdata(path="rw_bys20211227170900/02_scf/enerlog"):
    import os
    import re
    a=open(path,"rb").readlines()
    print(path)
    force_value = int(re.findall(r'\d+',str(a[-1]))[-1])
    print(force_value)
    return force_value
def read_enerdata(path="rw_bys20211227170900/02_scf/enerlog"):
    import os
    import re
    a=open(path,"rb").readlines()
    force_value = (re.findall(r'-\d+.\d+',str(a[-1]))[-1])
    return float(force_value)



import pandas as pd
import os
idlist = []
fvlist = []
enlist = []
df = pd.DataFrame()
dirlist = os.listdir("./")
for i in dirlist:
   # print(i)
    try:
          fv = read_loopdata(path=str(i)+"/01_relax/01_do/loopdata")
     #   ener = read_enerdata(path=str(i)+"/02_scf/enerlog")
          print(i,fv)
          idlist.append(i)
          fvlist.append(fv)
    except:
            pass

     #   enlist.append(ener)
df["id"] = idlist
df["fv"] = fvlist
#df["en"] = enlist






df2 = df.sort_values(by="fv")
df2.to_csv("./cac_log.csv",index=None)



