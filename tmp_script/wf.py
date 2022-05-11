import os, sys
import shutil
import time
submission_structure="./structure"
submission_stdfile="./demo"
submission_catalogue="./computing_directory"
submission_logfile="./submission_log"
node_number = 3

if not os.path.isdir(submission_catalogue):
    os.mkdir(submission_catalogue)
if not os.path.isdir(submission_logfile):
    os.mkdir(submission_logfile)

def std_process(posname):  ## 将demo文件夹拷入computing_directory文件夹，再将待计算结构拷入新生成的计算命名文件夹的通用过程
    os.system(f'cp -r ./demo computing_directory/{posname}')   ## 主要是INCAR和bash脚本(submit.lsf)
    shutil.copyfile(f"./structure/{posname}",f"./computing_directory/{posname}/POSCAR")   ## 待计算的结构命名为posname，内容是POSCAR文件

def submit(submit_dir):   ##告知要提交计算的目录，提交并记录
    vaspdone = 0
    mine = os.getcwd() # 记录当前位置
    os.chdir(mine) # 回到自己目录 确保安全
    os.chdir(submit_dir) # 进入计算目录
    os.system('bsub< submit.lsf')   ## 和提交排队系统的指令要一致,提交脚本命名为submit.lsf
    os.chdir(mine) # 回到自己目录 确保安全
    oname = "./cac.log"
    with open(oname, 'a') as t:
        print(f"submit the {submit_dir} stat 1",file=t)    ## 提示开始计算了 状态为1 占着节点
        #print(int(0),file=t)
        #print('Submission submitted', submit_dir,file=submission.submission_logfile)
    while abs(vaspdone)<1:
        if os.path.isfile(f'{submit_dir}/already_done'):  ## 脚本里要注意 计算完最后touch一个标记done文件
            print(f"{submit_dir} is done")
            vaspdone = 1
    with open(oname, 'a') as t:
        print(f"submit the {submit_dir} stat -1",file=t)    ## 提示计算结束了 状态为-1 不占节点


def high_throughput(submission_structure):   ##单节点 作为多节点的baseline
    errlog = "./hverr.log"
    for _ in os.listdir(submission_structure):
        try:
            std_process(_)
            submit(f'{submission_catalogue}/{_}')
        except Exception:
            with open(errlog, 'a') as t:
                print(f"{_} is not done",file=t)

def mut_high_throughput_monitor(node_number):  ##多节点
    errlog = "./mhv_err.log"
    _ = os.listdir(submission_structure)[0]
    std_process(_)
    submit(f'{submission_catalogue}/{_}')
    time.sleep(10)
    cac_list = os.listdir(submission_structure)[1:]  ##要计算的poscar的总的集合
    time.sleep(10)
    while True:
            htm = open("./cac.log",'a')
            nodelist = [int(c.split()[-1]) for c in htm.readlines()]
            run_node = sum(nodelist)
            if run_node < node_number:
                for i in (cac_list):
                    try:
                        std_process(i)
                        time.sleep(3)   ## std过程有copy文件夹的行为，所以要等待一会
                        submit(f'{submission_catalogue}/{i}')
                        cac_list.remove(i)
                    except Exception:
                        print("std_p err")
                        with open(errlog, 'a') as t:
                            print(f"{i} is not done",file=t)
            time.sleep(30)   ## 每隔30秒看一眼

mut_high_throughput_monitor(3)