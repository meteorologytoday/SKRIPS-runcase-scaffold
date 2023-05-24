#!/bin/bash

#SBATCH --job-name="case01_032.cpl"
#SBATCH --output="case01_032.cpl.%j.%N.out"
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --export=ALL
#SBATCH -t 12:00:00

source $HOME/.bashrc_skrips

nproc_ocn=4
nproc_atm=4
nproc_ttl=$(( $nproc_ocn + $nproc_atm ))

./Allclean

for model in SKRIPS mitGCM WRF mitGCM_bin; do
    ln -sf ../caseInput/$model/* .
done

# data.exf is different for standalone and coupled run
rm -f data.exf.standalone
mv data.exf.cpl data.exf

ln -sf ../coupledCode/esmf_application .

# ============================== 
# This section wants to get a reasonable
# heat flux for the first timestep

cp $WRF_DIR/main/wrf.exe .
cp ../../runWRF/wrfbdy_d01 . 
cp ../../runWRF/wrfinput_d01 .
cp ../../runWRF/wrflowinp_d01 .
python3 updateLowinp.py


# temporarily use an alternative wrf namelist
# that only outputs a short timestep
python3 wrf_namelist_short_run.py --input namelist.input.skrips --output namelist.input.tmp --overwrite
python3 wrf_namelist_rm_aux5.py   --input namelist.input.tmp --output namelist.input --overwrite

mpirun -np $nproc_atm ./wrf.exe

python3 updateHFlux.py --input wrfout_d01_2018-01-02_00:00:00 --time 6

mkdir init_find_heatflux_run
mv wrfout* init_find_heatflux_run/

# ============================== 

cp namelist.input.skrips namelist.input
echo "running coupled MITgcm--WRF simulation.."
mpirun -np $nproc_ttl ./esmf_application &> log.esmf 
