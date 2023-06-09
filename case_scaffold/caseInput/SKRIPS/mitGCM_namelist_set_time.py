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

####################################
files = genInOut("data")
print("Reading file: %s" % (files["in"],))
in_nml_data = parser.read(files["in"])


in_nml_data["PARM05"]["uVelInitFile"]    = "init_cond_U_%s.bin" % (run_datetimes["start_datetime"][2],)
in_nml_data["PARM05"]["vVelInitFile"]    = "init_cond_V_%s.bin" % (run_datetimes["start_datetime"][2],)
in_nml_data["PARM05"]["hydrogThetaFile"] = "init_cond_T_%s.bin" % (run_datetimes["start_datetime"][2],)
in_nml_data["PARM05"]["hydrogSaltFile"]  = "init_cond_S_%s.bin" % (run_datetimes["start_datetime"][2],)

print("Writing file: %s" % (files["out"],))
in_nml_data.end_comma = True
in_nml_data.write(files["out"], force=True)



####################################
files = genInOut("data.obcs")
print("Reading file: %s" % (files["in"],))
in_nml_data = parser.read(files["in"])


for bnd_short, bnd_long in [
    ("N", "north"),
    ("S", "south"),
    ("E", "east"),
    ("W", "west"),
]:

    for varname in ["U", "V", "T", "S"]:

        in_nml_data["OBCS_PARM01"]["OB%s%sFile" % (bnd_short, varname) ] = "open_bnd_%s_%s_%s_%s.bin" % (
            varname,
            run_datetimes["start_datetime"][2],
            run_datetimes["end_datetime"][2],
            bnd_long,
        )

print("Writing file: %s" % (files["out"],))
in_nml_data.end_comma = True
in_nml_data.write(files["out"], force=True)

####################################
files = genInOut("data.exf")
print("Reading file: %s" % (files["in"],))
in_nml_data_exf = parser.read(files["in"])

for bnd in ["N", "E", "W", "S"]:
    in_nml_data_exf["EXF_NML_OBCS"]["obcs%sstartdate1" % (bnd,)] = run_datetimes["start_datetime"][0]
    in_nml_data_exf["EXF_NML_OBCS"]["obcs%sstartdate2" % (bnd,)] = run_datetimes["start_datetime"][1]

print("Writing file: %s" % (files["out"],))
in_nml_data_exf.end_comma = True
in_nml_data_exf.write(files["out"], force=True)


####################################
files = genInOut("data.cal")
print("Reading file: %s" % (files["in"],))
in_nml_data_cal = parser.read(files["in"])

in_nml_data_cal["CAL_NML"]["startDate_1"] = run_datetimes["start_datetime"][0]
in_nml_data_cal["CAL_NML"]["startDate_2"] = run_datetimes["start_datetime"][1]

print("Writing file: %s" % (files["out"],))
in_nml_data_cal.end_comma = True
in_nml_data_cal.write(files["out"], force=True)

####################################
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
]:
    skrips_rc_file.setValue(key, val)

print("Writing file: %s" % (files["out"],))
skrips_rc_file.write(filename=files["out"], overwrite=True)


