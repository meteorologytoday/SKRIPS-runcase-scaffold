#!/bin/bash

#SBATCH --job-name="case01_032.Jan"
#SBATCH --output="case01_032.cpl.%j.%N.out"
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=24
#SBATCH --export=ALL
#SBATCH -t 12:00:00



source setting.sh
source $SKRIPS_ENV

nproc_ttl=$(( $nproc_ocn + $nproc_atm ))

./Allclean


ln -sf $caseroot/caeInput/mitGCM_bin/${start_date}/* .

for model in SKRIPS mitGCM WRF; do
    cp $caseroot/caseInput/$model/* .
done


# data.exf is different for standalone and coupled run
rm -f data.exf.standalone
mv data.exf.cpl data.exf

ln -sf ../../SKRIPS_program/coupledCode/esmf_application .

# ============================== 
# This section wants to get a reasonable
# heat flux for the first timestep
cp $WRF_DIR/main/wrf.exe .
cp ../runWRF/wrfbdy_d01 . 
cp ../runWRF/wrfinput_d01 .
cp ../runWRF/wrflowinp_d01 .
python3 updateLowinp.py


# temporarily use an alternative wrf namelist
# that only outputs a short timestep
python3 wrf_namelist_set_sim_time.py --input namelist.input.skrips --output namelist.input.skrips --overwrite --start-date $start_date --end-date $end_date  --run_days $run_days
python3 wrf_namelist_short_run.py --input namelist.input.skrips --output namelist.input --overwrite
python3 wrf_namelist_rm_aux5.py   --input namelist.input --output namelist.input --overwrite

# modify mitGCM time
python3 mitGCM_namelist_set_time.py --input-dir $( realpath . ) --start-date $start_date --end-date $end_date


echo "running coupled WRF-only simulation to get initial heat flux..."
mpirun -np $nproc_atm ./wrf.exe

python3 updateHFlux.py --input wrfout_d01_${start_date}_00:00:00 --time 6

mkdir init_find_heatflux_run
mv wrfout* init_find_heatflux_run/

# ============================== 

cp namelist.input.skrips namelist.input
echo "running coupled MITgcm--WRF simulation..."
mpirun -np $nproc_ttl ./esmf_application &> log.esmf 
