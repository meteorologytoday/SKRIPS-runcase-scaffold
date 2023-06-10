import f90nml
import argparse
import json
from datetime import datetime
import skrips_rc

parser = argparse.ArgumentParser(description='This program modifies the calendar time necessary for SKRIPS to run correctly, including data.exf, data.cal, and namelist.rc . Also, it modifies data initial files\' names.')

parser.add_argument('--input-dir', type=str, required=True, help='Input directory')
parser.add_argument('--output-dir', type=str, default="", help='Output directory, default is the same as `input-dir`')
parser.add_argument('--start-date',  type=str, default="", help='start date')
parser.add_argument('--end-date',    type=str, default="", help='end date')
parser.add_argument('--nproc-ocn',   type=int, required=True, help='Number of MITGCM cpu')
parser.add_argument('--nproc-atm',   type=int, required=True, help='Number of WRF cpu')

args = parser.parse_args()


if args.output_dir == "":
    args.output_dir = args.input_dir

print("Input directory  : %s" % (args.input_dir,))
print("Output directory : %s" % (args.output_dir,))

print(args)

def genInOut(filename):
    
    return {
        "in"  : "%s/%s" % (args.input_dir,  filename,),
        "out" : "%s/%s" % (args.output_dir, filename,),
    }


start_datetime = datetime.strptime(args.start_date, "%Y-%m-%d")
end_datetime   = datetime.strptime(args.end_date,   "%Y-%m-%d")

run_datetimes = dict(
    start_datetime = ( int(start_datetime.strftime("%Y%m%d")), int(start_datetime.strftime("%H%M%S")), start_datetime.strftime("%Y-%m-%d_%H")),
    end_datetime   = ( int(end_datetime.strftime("%Y%m%d")),   int(end_datetime.strftime("%H%M%S")),   end_datetime.strftime("%Y-%m-%d_%H")),
)

parser = f90nml.Parser()
parser.comment_tokens += "#"

files = genInOut("namelist.rc")
print("Reading file: %s" % (files["in"],))
skrips_rc_file = skrips_rc.SKRIPS_rc(files["in"]).read()

for key, val in [
    ("StartYear",   start_datetime.strftime("%Y")),
    ("StartMonth",  start_datetime.strftime("%m")),
    ("StartDay",    start_datetime.strftime("%d")),
    ("StartHour",   start_datetime.strftime("%H")),
    ("StartMinute", start_datetime.strftime("%M")),
    ("StartSecond", start_datetime.strftime("%S")),
    ("StopYear",    end_datetime.strftime("%Y")),
    ("StopMonth",   end_datetime.strftime("%m")),
    ("StopDay",     end_datetime.strftime("%d")),
    ("StopHour",    end_datetime.strftime("%H")),
    ("StopMinute" , end_datetime.strftime("%M")),
    ("StopSecond" , end_datetime.strftime("%S")),
    ("cpuOCN" ,     args.nproc_ocn),
    ("cpuATM" ,     args.nproc_atm),
]:
    skrips_rc_file.setValue(key, val)

print("Writing file: %s" % (files["out"],))
skrips_rc_file.write(filename=files["out"], overwrite=True)


