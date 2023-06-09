import f90nml
import argparse
import json
import datetime

parser = argparse.ArgumentParser(description='This program converts namelist.input file of SKRIPS-WRF to WRF only\'s namelist.input. The main work is to remove `auxinput5` related variables from `time_control` namegroup.')

parser.add_argument('--input', type=str, required=True, help='Input namelist file')
parser.add_argument('--output', type=str, required=True, help='Input namelist file')
parser.add_argument('--run_days',    type=int, default=0, help='run_days')
parser.add_argument('--run_hours',   type=int, default=0, help='run_hours')
parser.add_argument('--run_minutes', type=int, default=0, help='run_minutes')
parser.add_argument('--run_seconds', type=int, default=0, help='run_seconds')
parser.add_argument('--start-date',  type=str, default="", help='start date')
parser.add_argument('--end-date',    type=str, default="", help='end date')
parser.add_argument('--overwrite', action="store_true")

args = parser.parse_args()


print("Input file: %s" % (args.input,))
print("Output file: %s" % (args.output,))

print(args)

run_datetimes = dict(
    start = datetime.strptime(args.start_date, "%Y-%m-%d"),
    end   = datetime.strptime(args.end_date,   "%Y-%m-%d"),
)

namegroup = 'time_control'

in_nml = f90nml.read(args.input)

for mark in ['start', 'end']:
    for t_attr in ['year', 'month', 'day', 'hour', 'minute', 'second']:
        nml_attr = "%s_%s" % (mark, t_attr, )
        in_nml[namegroup][nml_attr] = getattr(run_datetimes[mark], t_attr)

for varname in ["run_days", "run_hours", "run_minutes", "run_seconds"]:
    in_nml[namegroup][varname] = getattr(args, varname)

print("Writing file: %s" % (args.output,))
in_nml.end_comma = True
in_nml.write(args.output, force=args.overwrite)



