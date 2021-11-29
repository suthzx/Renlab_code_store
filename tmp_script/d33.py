def get_pio_tensor(path="05_becs/OUTCAR"):
    """
    """
    import re
    import numpy as np 
    with open(path) as f:
        c= f.readlines()
    # 找到倒数两个压电矩阵的首行
    row = 0
    lines = []
    for i in c:
        if "PIEZOELECTRIC TENSOR" in i:
            lines.append(row)
        row = row +1

    arrays = []
    for r in lines[-2:]:
        #print(r)
        x = c[r +3]
        y = c[r +4]
        z = c[r +5]
        x_line = [i for i in re.split("\\s+",x)[2:8]]
        y_line = [i for i in re.split("\\s+",y)[2:8]]
        z_line = [i for i in re.split("\\s+",z)[2:8]]
        array = np.array([x_line,y_line,z_line]).astype(np.float64)
        #print(array)
        arrays.append(array)
    # 两个矩阵加和
    pie_tensor = arrays[0]+arrays[1]
    #print("pie_tensor before exchange:",pie_tensor)
    # 换位置XY 到最后
    pie_tensor = pie_tensor[:,[0,1,2,4,5,3]]
    #print("pie_tensor final:",pie_tensor)
    return pie_tensor
def get_sij(path="06_ela/vaspkit.log"):
    import re
    import numpy as np
    with open(path) as f:
        c= f.readlines()
    row = 0
    ct_line_list = []
    for i in c:
        if "Compliance Tensor" in i:
            for add_line_index in range(1,7):
                ct_line = re.split("\\s+",c[row+add_line_index])[1:7]
                ct_line_list.append(ct_line)
            #print(c[row:row+7])
        row =row+1
    sij = np.array(ct_line_list).astype(np.float64)
    #print(sij)
    return sij
    
    
def get_cij(path="06_ela/vaspkit.log"):
    import re
    import numpy as np
    with open(path) as f:
        c= f.readlines()
    row = 0
    ct_line_list = []
    for i in c:
        if "Stiffness Tensor C_ij" in i:
            for add_line_index in range(1,7):
                ct_line = re.split("\\s+",c[row+add_line_index])[1:7]
                ct_line_list.append(ct_line)
            #print(c[row:row+7])
        row =row+1
    cij = np.array(ct_line_list).astype(np.float64)
    print("c33",cij[2,2])
    return cij
    
def read_energy(path):
    path=  path
    import re
    with open(path) as f:
            c= f.readlines()
    pattern = re.compile(r'E0=(.*)d')
    result1 = pattern.findall(c[0])
    print("energy",result1[0])
    return result1[0]
 
def get_d33(path_sij="06_ela/vaspkit.log",path="05_becs/OUTCAR"):
    import numpy as np
    sij = get_sij(path_sij)
    pij = get_pio_tensor(path)
    print(np.matmul(pij,sij))
    print("d33 :",np.matmul(pij,sij)[2,2]*1000)
    return np.matmul(pij,sij)
    

    
    
    
get_d33(path_sij="./06_ela/vaspkit.log",path="./05_becs/OUTCAR")
get_cij("./06_ela/vaspkit.log")
read_energy("./02_scf/energy")