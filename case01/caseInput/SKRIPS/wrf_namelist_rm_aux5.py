import f90nml
import argparse
import json

parser = argparse.ArgumentParser(description='This program converts namelist.input file of SKRIPS-WRF to WRF only\'s namelist.input. The main work is to remove `auxinput5` related variables from `time_control` namegroup.')

parser.add_argument('--input', type=str, required=True, help='Input namelist file')
parser.add_argument('--output', type=str, required=True, help='Input namelist file')
parser.add_argument('--overwrite', action="store_true")

args = parser.parse_args()


print("Input file: %s" % (args.input,))
print("Output file: %s" % (args.output,))


namegroup = 'time_control'

in_nml = f90nml.read(args.input)

print("Original namegroup `%s`" % (namegroup,))
print(json.dumps(in_nml[namegroup], indent=4))


for varname in [
    "auxinput5_inname",
    "auxinput5_interval_s",
    "auxinput5_end_d",
    "io_form_auxinput5",
    "auxhist5_outname",
    "auxhist5_interval_s",
    "auxhist5_end_d",
    "io_form_auxhist5",
]:
    print("Removing variable: %s" % (varname,))
    del in_nml[namegroup][varname]




print("Writing file: %s" % (args.output,))
in_nml.end_comma = True
in_nml.write(args.output, force=args.overwrite)



