import re
import time
import requests
import threading
import multiprocessing
import contextlib
import os
with contextlib.suppress(Exception):
    os.mkdir("./oqmddata")
class ThreadTask(threading.Thread):
    def __init__(self, func, args=()):
        super(ThreadTask, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def get_jy_3dallposcar(start,end):
    for i in range(start,end):
        try:
            u = f"https://oqmd.org/materials/entry/{i}"
            
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
                                    ,"cookie":"__gads=ID=014026dedec37c01:T=1595342001:S=ALNI_MasVWhAiEcBOmvnzCIDi5M6zPpmJg; _ga=GA1.2.1228056970.1595342002; _gid=GA1.2.1719295543.1595342002"}
            response = requests.get(u, headers=headers)
            time.sleep(5)
            #response.text
            fml = re.findall(r'href="/materials/composition/(.*?)"', response.text)
            ener = float(re.findall(r'fine_relax</a></td>.*?(-.*?)<', response.text,re.S)[0])
            oname = f"./oqmd{start}.log"
            with open(oname, 'a') as t:
                print(fml,"=",ener,file=t)
        except:
            ename = f".oqmdloss{start}.log"
            with open(ename, 'a') as t:
                print(f"{i}err",file=t)
                
                
get_jy_3dallposcar(5555,100000)