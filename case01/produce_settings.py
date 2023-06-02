import argparse
import os
import pandas as pd

def pleaseRun(cmd):
    print(">> %s" % cmd)
    os.system(cmd)


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input',  type=str, required=True, help='Input file')
parser.add_argument('--output', type=str, required=True, help='Output file')
parser.add_argument('--SKRIPS_ENV', type=str, default='$HOME\/.bashrc_skrips', help='Path of skrips environment variable file.')
parser.add_argument('--CASEROOT', type=str, required=True, help='Path to the case root folder.')
parser.add_argument('--START_DATE', type=str, required=True, help='Start date of the boundary condition for WRF.')
parser.add_argument('--END_DATE', type=str, required=True, help='End date of the boundary condition for WRF.')
parser.add_argument('--RUN_DAYS', type=int, default=1, help='Simulation days.')

parser.add_argument('--NPROC_OCN', type=int, default=1, help='Number of cores to run the ocean model.')
parser.add_argument('--NPROC_ATM', type=int, default=1, help='Number of cores to run the atmosphere model.')

args = parser.parse_args()

print(args)

replaced_variables = [
    "SKRIPS_ENV",
    "CASEROOT",
    "START_DATE",
    "END_DATE",
    "RUN_DAYS",
    "NPROC_OCN",
    "NPROC_ATM",
]


args.CASEROOT = args.CASEROOT.replace('/', '\/')


args.START_DATE = pd.Timestamp(args.START_DATE).strftime("%Y-%m-%d")
args.END_DATE   = pd.Timestamp(args.END_DATE).strftime("%Y-%m-%d")



sed_cmds = []
for varname in replaced_variables:

    sed_cmds.append("s/_____%s_____/%s/g" % (varname, getattr(args, varname)))


sed_cmd_str = "sed '%s' %s > %s" % (
    "; ".join(sed_cmds),
    args.input,
    args.output,
)

pleaseRun(sed_cmd_str)

