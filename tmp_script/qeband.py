import matplotlib.pyplot as plt

ax1 = plt.subplot2grid((4,4),(0,0),colspan = 4,rowspan = 4)


filename = 'Si.freq'
f = open (filename)
lines = f.readlines()
f.closed



date=[]
for line in lines:
    dateline = line.rstrip()
    long = len(dateline.split(' ')) 
    k1 = []    
    for i in range(long):
        itme = line.split(' ')[i]
        if  itme :
            date.append(itme)

nband = int(date[2])

nkpoints = int(date[4])
kp = [0,0,0]
kpoint=0
kpoints=[]
enegy=[]
fermi = 0
for i in range(nkpoints):         
    kp_1 = kp
    kp=[float(date[6+i*nband+3*i]),float(date[7+i*nband+3*i]),float(date[8+i*nband+3*i])]
    dkp = [kp[0]-kp_1[0],kp[1]-kp_1[1],kp[2]-kp_1[2]]
    dkpoint = (dkp[0]**2+dkp[1]**2+dkp[2]**2)**0.5
    kpoint +=dkpoint
    kpoints.append(kpoint)  
    for j in range (nband):
        enegy.append(float(date[9+j+i*(nband+3)])-fermi)


for m in range(nband):
    enegy_1 = []
    for k in range(nkpoints):
        enegy_1.append(enegy[k*nband+m])
    ax1.plot(kpoints[:],enegy_1[:],linewidth=1,c='blue')


ax1.set_ylim(0,500)
ax1.set_xlim(min(kpoints),max(kpoints))
ax1.set_xlabel('Wave Vector')
ax1.set_ylabel('E-Ef(eV)')


plt.show()


