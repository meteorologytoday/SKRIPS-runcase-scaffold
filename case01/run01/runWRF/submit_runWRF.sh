#!/bin/bash

#SBATCH --job-name="case01_032"
#SBATCH --output="case01_032.%j.%N.out"
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL
#SBATCH -t 12:00:00

source $HOME/.bashrc_skrips


./Allclean
./AllInit


nproc=4

#This job runs with 1 node, 8 cores per node for a total of 8 cores.
# We use 8 MPI tasks.

cplpath=../runCPL.AO_shell/caseInput/SKRIPS 
python3 $cplpath/wrf_namelist_rm_aux5.py --input $cplpath/namelist.input.skrips --output namelist.input.tmp --overwrite
python3 $cplpath/wrf_namelist_short_run.py --input namelist.input.tmp --output namelist.input --overwrite




mpirun -np $nproc ./real.exe
#mpirun -np $nproc ./wrf.exe
