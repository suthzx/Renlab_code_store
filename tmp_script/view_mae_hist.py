###%config InlineBackend.figure_format = 'svg'
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_csv("./Energy.dat",sep="\t",header = None)
df.columns=["pwd","ener","un"]
df2 = df.sort_values(by='ener',ascending=False)
df2.to_csv("./ener_range.csv",index=None)
x_plt= np.linspace(1,100,len(df))
y_plt = df2["ener"]
plt.scatter(x_plt,y_plt,alpha=0.6)
plt.plot(x_plt,y_plt)
####%config InlineBackend.figure_format = 'svg'
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#设置字体和figure大小
plt.rcParams['font.family']='Arial'
plt.rcParams['font.size']=15
plt.figure(figsize=(10,7))
sns.set_palette("deep") #设置所有图的颜色，使用hls色彩空间
df = pd.read_csv("./Energy.dat",sep="\t",header = None)
df.columns=["pwd","ener","un"]
df2 = df.sort_values(by='ener',ascending=False)
df2.to_csv("./ener_range.csv",index=None)
x_plt= np.linspace(1,100,len(df))
y_plt = df2["ener"]
#plt.scatter(x_plt,y_plt,alpha=0.6)
#plt.plot(x_plt,y_plt)
#plt.hist(y_plt,alpha=0.5,bins=20)
#sns.kdeplot(y_plt,shade=True,vertical=False,gridsize=100,cut=2)
sns.set_style('white')
# sns.distplot(y_plt,bins=30,hist=True,rug=False,vertical=False,
#              norm_hist=True,
#              kde_kws={"lw":3 ,"alpha": 0.8,"linestyle":"-","color":"orange"},
#              hist_kws={ "alpha": 1})
sns.distplot(y_plt)
#plt.show()
plt.savefig("./ener_range.tif",dpi=300,bbox_inches="tight")
plt.savefig("./ener_range.png",dpi=300,bbox_inches="tight")