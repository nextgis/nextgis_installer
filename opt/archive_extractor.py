#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS installer
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
## Copyright (c) 2018 NextGIS <info@nextgis.com>
## License: GPL v.2
##
## Autoextractor script. Extracts all archives in folder, replace existing
## directory and delete archive
##
################################################################################

import os
import sys
import argparse
import shutil
import zipfile

parser = argparse.ArgumentParser(description='Autoextractor. NextGIS desktop software installer.')
parser.add_argument('-d', dest='dir', required=False, help='Directory to find zip archives')
args = parser.parse_args()

parse_dir = ''
if args.dir is None:
    parse_dir = os.getcwd()
else:
    parse_dir = args.dir

archives = []

# 1. Read current directory contents
for f in os.listdir(parse_dir):
    if '.zip' in f:
        archives.append(f)

# 2. Create zip list
for archive in archives:
    print 'Process ' + archive

    base_name = os.path.splitext(archive)[0]
    dir_path0 = os.path.join(parse_dir, base_name)
    dir_path1 = os.path.join(parse_dir, base_name + '.1')
    dir_path2 = os.path.join(parse_dir, base_name + '.2')

# 3. Rename correspondent folders original -> original.1 -> original.2 -> /dev/null
    if os.path.exists(dir_path2):
        shutil.rmtree(dir_path2)

    if os.path.exists(dir_path1):
        os.rename(dir_path1, dir_path2)

    if os.path.exists(dir_path0):
        os.rename(dir_path0, dir_path1)

    zip_path = os.path.join(parse_dir, archive)

# 4. Extract zip. If failed rename original.2 -> original.1 -> original
    try:
        zip_ref = zipfile.ZipFile(zip_path, 'r')
        zip_ref.extractall(parse_dir)
        zip_ref.close()
        os.remove(zip_path)
        print 'Process ' + archive + ' successfully'
    except:
        print 'Process ' + archive + ' failed. Roll back'
        # Roll back
        if os.path.exists(dir_path2):
            os.rename(dir_path2, dir_path1)
        if os.path.exists(dir_path1):
            shutil.rmtree(dir_path0)
            os.rename(dir_path1, dir_path0)
