#!/usr/bin/env python

import argparse
import subprocess

parser = argparse.ArgumentParser()

parser.add_argument(
    "--url",
    default="http://portal.nersc.gov/project/desi/users/govinda/20160816/",
    help="URL of the data repository")

parser.add_argument(
    "--output_dir",
    default=None,
    help="Download directory")

parser.add_argument("--cut_dirs", default="5")

args = parser.parse_args()

cmd = (
    "wget -r --cut-dirs %s -nH --reject index.html* "
    "--accept-regex='.*(\/[0-9]+)\/([0-9]+).*' %s "
    "&& rm robots.txt"
) % (args.cut_dirs, args.url)

print('Executing: %s' % cmd)

process = subprocess.Popen(cmd, shell=True, cwd=args.output_dir)
process.wait()

exit()
