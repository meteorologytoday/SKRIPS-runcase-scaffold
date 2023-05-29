#!/bin/bash

#SBATCH --job-name="case01_032"
#SBATCH --output="case01_032.%j.%N.out"
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL
#SBATCH -t 12:00:00

source $HOME/.bashrc_skrips


nproc=4

mpirun -np $nproc ./real.exe
