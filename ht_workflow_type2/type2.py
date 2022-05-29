#!/bin/bash
#BSUB -q gold
#BSUB -o out.%J.txt
#BSUB -e error.%J.txt
#BSUB -J cal_A2B2_1
#BSUB -n 36
##BSUB -R "span[ptile=72]"
#BSUB -R "span[hosts=1]"

source /etc/profile
module load gold/compiler/intel/ps2018
module load gold/vasp/vasp544_avx512_intel2018
#Run MultiTheads per MPI Process
#-genv OMP_NUM_THREADS 1
export OMP_NUM_THREADS=1
######################################################################

outfilename=output1
dir0=`pwd`


for folder in cal-*
do
    cd $dir0
    cd $folder
    #防止脚本重复运行
    if [ ! -f "POTCAR" ]; then
        #生成POTCAR      ##为保证精度，KPOINTS在之后单独生成
        vaspkit -task 103
        wait

        ###优化3次
        ###制作文件夹
        mkdir {01_relax,02_scf,03_becs,04_ela,05_other}
        mkdir 01_relax/{01_do,02_copy}
        cp INCAR POSCAR POTCAR 01_relax/01_do/
        cd 01_relax/01_do/
        outfile=../../$outfilename
        #1
        echo -e "102\n2\n0.015" | vaspkit
        wait
        sed -i "s/^.*\\bEDIFF\\b.*$/ EDIFF = 1E-5/" INCAR
        sed -i "s/^.*\\bISIF\\b.*$/ ISIF = 3/" INCAR
        sed -i "s/^.*\\bIBRION\\b.*$/ IBRION = 2/" INCAR
        sed -i "s/^.*\\bPOTIM\\b.*$/ POTIM = 0.2 /" INCAR
        out=opt1__________________________________________
        echo -e $out >>$outfile
        mpirun -genv I_MPI_FABRICS shm -bootstrap lsf vasp_std >>$outfile
        wait
        #2
        echo -e "102\n2\n0.015" | vaspkit
        wait
        sed -i "s/^.*\\bEDIFF\\b.*$/ EDIFF=1E-7/" INCAR
        out=opt2__________________________________________
        echo -e "\n"$out >>$outfile
        mpirun -genv I_MPI_FABRICS shm -bootstrap lsf vasp_std >>$outfile
        wait
        #3
        echo -e "102\n2\n0.015" | vaspkit
        wait
        sed -i "s/^.*\\bEDIFF\\b.*$/ EDIFF=1E-7/" INCAR
        sed -i "s/^.*\\bIBRION\\b.*$/ IBRION = 1/" INCAR
        sed -i "s/^.*\\bPOTIM\\b.*$/ POTIM = 0.1 /" INCAR
        out=opt3__________________________________________
        echo -e "\n"$out >>$outfile
        mpirun -genv I_MPI_FABRICS shm -bootstrap lsf vasp_std >>$outfile
        wait
        
        cp CONTCAR INCAR KPOINTS POSCAR POTCAR  ../02_copy/
        #判断结构是否优化完成        
        grep "reached required accuracy - stopping structural energy minimisation" OUTCAR || continue 

        ###自洽
        cp CONTCAR INCAR POTCAR ../../02_scf/
        cd ../../02_scf/
        mv CONTCAR POSCAR
        echo -e "102\n2\n0.015" | vaspkit
        wait
        outfile=../$outfilename

        sed -i "s/^.*\\bISTART\\b.*$/ ISTART = 0/" INCAR
        sed -i "s/^.*\\bICHARG\\b.*$/ ICHARG = 2/" INCAR
        sed -i "s/^.*\\bLWAVE\\b.*$/ LWAVE = .TRUE./" INCAR
        sed -i "s/^.*\\bLCHARG\\b.*$/ LCHARG = .TRUE./" INCAR
        sed -i "s/^.*\\bNSW\\b.*$/ NSW = 0/" INCAR
        sed -i "s/^.*\\bIBRION\\b.*$/ IBRION = -1/" INCAR
        sed -i "s/^.*\\bISIF\\b.*$/ ISIF = 2/" INCAR
        sed -i "/LCHARG/ a\ LORBIT = 11" INCAR
        out=scf__________________________________________
        echo -e "\n\n"$out >>$outfile
        mpirun -genv I_MPI_FABRICS shm -bootstrap lsf vasp_std >>$outfile
        wait

        EMAX=$(sed -n 6p DOSCAR | awk '{print($1)}')
        EMIN=$(sed -n 6p DOSCAR | awk '{print($2)}')
        NEDOS=$(echo "scale=0;($EMAX - $EMIN)/0.01" | bc -l -q);


        ###准备能带、压电、弹性模量的文件
        cd ../
        cp INCAR  03_becs/
        cp INCAR  VPKIT.in  04_ela/
        cd 02_scf
        cp POSCAR  POTCAR  ../03_becs/
        cp POSCAR  POTCAR  ../04_ela/


        ###压电
        cd ../03_becs
        echo -e "102\n2\n0.015" | vaspkit
        wait
        sed -i "s/^.*\\bISTART\\b.*$/ ISTART = 0/" INCAR
        sed -i "s/^.*\\bICHARG\\b.*$/ ICHARG = 2/" INCAR
        sed -i "s/^.*\\bNSW\\b.*$/ NSW = 1/" INCAR
        sed -i "/ISMEAR/ a\ LEPSILON  = TRUE" INCAR
        sed -i "s/^.*\\bIBRION\\b.*$/ IBRION = 8/" INCAR
        sed -i "s/^.*\\bNPAR\\b.*$/ #NPAR=4/" INCAR
        sed -i "s/^.*\\bNCORE\\b.*$/ #NCORE=12/" INCAR
        sed -i "s/^.*\\bLWAVE\\b.*$/ LWAVE  = .FALSE./" INCAR
        sed -i "s/^.*\\bLCHARG\\b.*$/ LCHARG = .FALSE./" INCAR
        sed -i "s/^.*\\bEDIFF\\b.*$/ EDIFF=1E-6/" INCAR

        out=becs__________________________________________
        echo -e "\n\n"$out >>$outfile
        mpirun -genv I_MPI_FABRICS shm -bootstrap lsf vasp_std >>$outfile
        wait
        grep -5 'PIEZOELECTRIC TENSOR IONIC CONTR  for field in x, y, z'  OUTCAR >tensor.log
        wait


        ###弹性模量
        cd ../04_ela
        echo -e "102\n2\n0.015" | vaspkit
        wait
        outfile=../../$outfilename

        sed -i "s/^.*\\bIBRION\\b.*$/ IBRION = 1/" INCAR
        sed -i "s/^.*\\bISIF\\b.*$/ ISIF = 2/" INCAR
        sed -i "s/^.*\\bEDIFF\\b.*$/ EDIFF=1E-6/" INCAR
        vaspkit -task 201
        wait

        dir=`pwd`
        echo $dir

        function getdir(){
            echo $1
            for file in $1/*
            do
                if test -d $file
                then
                    arr=(${arr[*]} $file)
                    cd $file
                    out="ela"$file"__________________________________________"
                    echo -e "\n\n"$out >>$outfile
                    mpirun -genv I_MPI_FABRICS shm -bootstrap lsf vasp_std >>$outfile
                    wait
                    if [ -f "OUTCAR" ]; then
                        grep "reached required accuracy - stopping structural energy minimisation" OUTCAR || break         
                    fi
                    cd $dir
                    getdir $file
                fi
            done
            }
        getdir . 

        wait
        cd $dir
        sed -i '1s/1/2/g' VPKIT.in

        vaspkit -task 201 >vaspkit.log
        wait

        grep -16 'Compliance Tensor S_ij'  vaspkit.log >ela.log

        ###输出压电参数
        cd ../
        python d33.py  > pied33.txt
    fi
    cd ../
    python DATA.py
done