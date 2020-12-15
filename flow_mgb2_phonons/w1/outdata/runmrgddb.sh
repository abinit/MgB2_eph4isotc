#!/bin/bash
cd /scratch/users/g/m/gmatteo/MgB2_eph4isotc/flow_mgb2_phonons/w1/outdata
# Load Modules
module purge
module load releases/2018b 2>> mods.err
module load intel/2018b 2>> mods.err
module load iimpi/2018b 2>> mods.err
module load libxc/4.2.3-intel-2018b 2>> mods.err
module load netCDF-Fortran/4.4.4-intel-2018b 2>> mods.err

# OpenMp Environment
export OMP_NUM_THREADS=1
# Commands before execution
export OMP_NUM_THREADS=1
export PATH=$HOME/git_repos/abinit_rmms/_build_intel/src/98_main:$PATH
ulimit -s unlimited

mpirun  -n 1 mrgddb --nostrict < /scratch/users/g/m/gmatteo/MgB2_eph4isotc/flow_mgb2_phonons/w1/outdata/mrgddb.stdin > /scratch/users/g/m/gmatteo/MgB2_eph4isotc/flow_mgb2_phonons/w1/outdata/mrgddb.stdout 2> /scratch/users/g/m/gmatteo/MgB2_eph4isotc/flow_mgb2_phonons/w1/outdata/mrgddb.stderr
