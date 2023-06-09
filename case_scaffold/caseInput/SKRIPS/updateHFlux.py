#!/home/rus043/miniconda3/bin/python
import sys, os, os.path
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np
from scipy import interpolate
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True, help='Input wrfout file to set the heat flux.')
parser.add_argument('--time', type=int, default=0, help='The timeslice index. Default = 0')
args = parser.parse_args()

print("# Parameters read:")
print(args)

nIniStep = args.time

set_results = Dataset(args.input,'r',format='NETCDF4');
set_swupb = set_results.variables['SWUPB'][nIniStep,:,:]
set_swdnb = set_results.variables['SWDNB'][nIniStep,:,:]
set_lwupb = set_results.variables['LWUPB'][nIniStep,:,:]
set_lwdnb = set_results.variables['LWDNB'][nIniStep,:,:]
set_lh    = set_results.variables['LH'][nIniStep,:,:]
set_sh    = set_results.variables['HFX'][nIniStep,:,:]

ini_results = Dataset('wrfinput_d01','r+',format='NETCDF4');

"""
ini_swupb = ini_results.variables['SWUPB'][nIniStep,:,:]
ini_swdnb = ini_results.variables['SWDNB'][nIniStep,:,:]
ini_lwupb = ini_results.variables['LWUPB'][nIniStep,:,:]
ini_lwdnb = ini_results.variables['LWDNB'][nIniStep,:,:]
ini_lh = ini_results.variables['LH'][nIniStep,:,:]
ini_sh = ini_results.variables['HFX'][nIniStep,:,:]
"""

ini_results.variables['SWUPB'][0,:,:] = set_swupb
ini_results.variables['SWDNB'][0,:,:] = set_swdnb
ini_results.variables['LWUPB'][0,:,:] = set_lwupb
ini_results.variables['LWDNB'][0,:,:] = set_lwdnb
ini_results.variables['LH'][0,:,:]    = set_lh
ini_results.variables['HFX'][0,:,:]   = set_sh

ini_results.close()

print("new swupb: ", np.mean(set_swupb))
print("new swdnb: ", np.mean(set_swdnb))
print("new lwupb: ", np.mean(set_lwupb))
print("new lwdnb: ", np.mean(set_lwdnb))
print("new lh: ", np.mean(set_lh))
print("new sh: ", np.mean(set_sh))
