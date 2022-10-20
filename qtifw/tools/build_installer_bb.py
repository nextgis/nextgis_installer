#!/usr/bin/env python
#############################################################################
##
## Copyright (C) 2017 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the Qt Installer Framework.
##
## $QT_BEGIN_LICENSE:GPL-EXCEPT$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3 as published by the Free Software
## Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
## Modified by NextGIS for buildbot
## Copyright (C) 2018 NextGIS, <info@nextgis.com>
## Copyright (C) 2018 Dmitry Baryshnikov, <dmitry.baryshnikov@nextgis.com>
#############################################################################

import argparse
import os
import shutil
import string
import subprocess
import sys

args = {}

src_dir = ''
build_dir = ''
qmake = ''
vcvars = ''

def parse_arguments():
    global args

    parser = argparse.ArgumentParser(description='Build installer for installer framework.')
    parser.add_argument('--clean', dest='clean', action='store_true', help='delete all previous build artifacts')
    parser.add_argument('--qtdir', dest='qt_dir', required=True, help='path to qmake that will be used to build the tools')
    parser.add_argument('--make', dest='make', required=True, help='make command')

    args = parser.parse_args()

def init():
    global src_dir
    global build_dir
    global qmake
    global vcvars

    src_dir = os.path.dirname(os.getcwd())
    root_dir = os.path.dirname(src_dir)
    basename = os.path.basename(src_dir)
    build_dir = os.path.join(root_dir, basename + '_build')

    # This is buildbot run. Get absolute path.
    qt_dir = os.path.dirname(os.path.dirname(root_dir))
    qt_dir = os.path.join(qt_dir, args.qt_dir)
    abs_qt_dir = os.path.abspath(qt_dir)
    print('abs_qt_dir: ' + abs_qt_dir)
    for subdir in os.listdir(abs_qt_dir):
        test_path = os.path.join(abs_qt_dir, subdir, 'bin')
        if os.path.isdir(test_path):
            qmake = os.path.join(test_path, 'qmake')
            break

    print('qmake: ' + qmake)
    print('source dir: ' + src_dir)
    print('build dir: ' + build_dir)

    if args.clean and os.path.exists(build_dir):
        print('delete existing build dir ...')
        shutil.rmtree(build_dir)
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    if sys.platform == 'win32':
        # find vcvars script
        vcvars_paths = [
            'C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\VC\\\Auxiliary\\\Build\\',
        ]

        for vcvars_path in vcvars_paths:
            if os.path.exists(vcvars_path + '\\vcvarsall.bat'):
                vcvars = '\"' + vcvars_path + '\\vcvarsall.bat\" x64'
                break


def run(args):
    if sys.platform == 'win32' and vcvars is not None and vcvars != '':
        args = vcvars + ' && ' + args

    print('calling ' + args)
    subprocess.check_call(args, shell=True)

def build():
    print('building sources ... in ' + build_dir)
    os.chdir(build_dir)
    run('\"' + qmake + '\" CONFIG+=release \"' + src_dir + '\"')
    run(args.make)
    if sys.platform == 'win32':
        # execute mt.exe to embed a manifest inside the application to avoid error such as missing MSVCP90.dll when the application is started on other computers
        # os.chdir(os.path.joint(build_dir, 'release'))
        # run('mt.exe -manifest Hello.exe.manifest -outputresource: Hello.exe')
        test_path = os.path.join(os.getenv("USERPROFILE"), 'source', 'bin')
        if os.path.exists(test_path):
            print('It must not happen, but though qmake not honor DESTDIR, let\'s move directory there')
            shutil.move(test_path, build_dir)

parse_arguments()
init()
build()
