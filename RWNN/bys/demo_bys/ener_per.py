
def get_ener_peer(path1 = "./OSZICAR",path2 = "./POSCAR"):
    
    f=open(path1,'r+')
    flist=f.readlines()
    totener = float(flist[-1].strip().split()[4])
    
    f=open(path2,'r+')
    flist=f.readlines()
    a = 0
    for i in flist[6].strip().split():
        a = a + int(i)
    ener_peer_a = totener/a
    print(ener_peer_a)
    return ener_peer_a

get_ener_peer()
