#!/usr/bin/env python
# coding: utf-8
# thsu0407@gmail.com
from ctgan import load_demo
import warnings
import pandas as pd
CUDA_LAUNCH_BLOCKING=1
warnings.filterwarnings("ignore")
data = pd.read_csv("./train_suth.csv",index=None)
data = data.drop(["v"],axis = 1)
# Names of the columns that are discrete
discrete_columns = ["e"+str(i) for i in range(en_cut)]+["inter","point"]
ctgan = CTGANSynthesizer(epochs=1000,verbose=True,batch_size = 128)
ctgan.fit(data, discrete_columns)
ctgan.save('ctgan-food-demand.pkl')
samples = ctgan.sample(10000)
samples.to_csv("look1w.csv",index=None)
