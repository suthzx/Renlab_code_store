import pandas as pd
import numpy as np
import matplotlib.pyplot as pl
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import random

def gaussian(x,*param):
    """
    0 - seita
    1 *- miu
    """
    return param[0]*np.exp(-((x-param[1])**2/(2*(param[0])**2)))
def gaussian_sample(x,y):
    max_number, _= find_peaks(y, height=0)
    max_number=max_number[0]##数组中第一个极大值对应的序号
    a=np.array([0,x[max_number],x[max_number-1],x[max_number-2],x[max_number-3],x[max_number+1],x[max_number+2],x[max_number+3]])
    b=np.array([0,y[max_number],y[max_number-1],y[max_number-2],y[max_number-3],y[max_number+1],y[max_number+2],y[max_number+3]])
    popt,pcov = curve_fit(gaussian,a,b,p0=[1,x[max_number]])
    y_fit=[]
    for i in range(len(x)):
        y_fit.append(gaussian(x[i],*popt))
    max_y_fit=y_fit[max_number]
    for i in range(len(x)):
        y_fit[i]=y_fit[i]/max_y_fit
        y_fit[i]=1-y_fit[i]
    sum=0
    for i in range(max_number+1):
        sum=sum+y_fit[i]
    ran=sum*random.random()
    count=0
    for i in range(max_number+1):
        if(count<ran):
            count=count+y_fit[i]
        else:
            re_num=i
            break
    index=re_num
    return x[re_num],y[re_num],index

df_data=pd.read_excel("xy.xlsx")
x=np.array(df_data["x"])
y=np.array(df_data["y"])
sample_x,sample_y,index=gaussian_sample(x,y)
