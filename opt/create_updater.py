#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS online/offline installer
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
## Copyright (c) 2016-2018 NextGIS <info@nextgis.com>
## License: GPL v.2
##
################################################################################

import os
import argparse
import sys
import subprocess
import string

args = {}
updater_repo = 'nextgis_updater'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKGRAY = '\033[0;37m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DGRAY='\033[1;30m'
    LRED='\033[1;31m'
    LGREEN='\033[1;32m'
    LYELLOW='\033[1;33m'
    LBLUE='\033[1;34m'
    LMAGENTA='\033[1;35m'
    LCYAN='\033[1;36m'
    WHITE='\033[1;37m'


def color_print(text, bold, color):
    if sys.platform == 'win32':
        print text
    else:
        out_text = ''
        if bold:
            out_text += bcolors.BOLD
        if color == 'GREEN':
            out_text += bcolors.OKGREEN
        elif color == 'LGREEN':
            out_text += bcolors.LGREEN
        elif color == 'LYELLOW':
            out_text += bcolors.LYELLOW
        elif color == 'LMAGENTA':
            out_text += bcolors.LMAGENTA
        elif color == 'LCYAN':
            out_text += bcolors.LCYAN
        elif color == 'LRED':
            out_text += bcolors.LRED
        elif color == 'LBLUE':
            out_text += bcolors.LBLUE
        elif color == 'DGRAY':
            out_text += bcolors.DGRAY
        elif color == 'OKGRAY':
            out_text += bcolors.OKGRAY
        else:
            out_text += bcolors.OKGRAY
        out_text += text + bcolors.ENDC
        print out_text


def parse_arguments():
    global args

    parser = argparse.ArgumentParser(description='Create NextGIS desktop software updater package.')
    parser.add_argument('-i', dest='installer_name', required=True, help='Installer name')
    parser.add_argument('-v', dest='version', required=True, help='updater version')
    parser.add_argument('--ftp_user', dest='ftp_user', required=True, help='FTP user name and password to fetch package.zip anv version.str files')
    parser.add_argument('--ftp', dest='ftp', required=True, help='FTP address with directories to fetch installer.exe package.zip anv version.str files')
    parser.add_argument('--ftpout_user', dest='ftpout_user', required=True, help='FTP user name and password to store package.zip anv version.str files')
    parser.add_argument('--ftpout', dest='ftpout', required=True, help='FTP address with directories to store package.zip anv version.str files')
    args = parser.parse_args()


def run(args):
    print 'calling ' + string.join(args)
    subprocess.check_call(args)


parse_arguments()
ftp = args.ftp
if ftp[-1:] != '/':
    ftp += '/'

# 1 Get installer exe
installer_name = args.installer_name
suffix = ''
if sys.platform == 'darwin':
    installer_name += '.dmg'
    suffix = 'mac'
elif sys.platform == 'win32':
    installer_name += '.exe'
    suffix = 'win'

run(('curl', '-u', args.ftp_user, ftp + installer_name, '-o', installer_name))

# 2 Install it to temp folder
tmp_dir = os.path.join(os.getcwd(), 'tmp')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

installer_exe = ''

if sys.platform == 'darwin':
    subprocess.check_output(['hdiutil', 'attach', os.path.join(os.getcwd(), installer_name)])
    installer_exe = os.path.join('/Volumes', 'NextGIS Setup', 'nextgis-setup.app', 'Contents', 'MacOS', 'nextgis-setup')
elif sys.platform == 'win32':
    installer_exe = os.path.join(os.getcwd(), installer_name)

# Create maintance tool package
# 1. Silent install created installer to temp folder (https://stackoverflow.com/a/34032216/2901140)

silent_install_dir = os.path.join(tmp_dir, 'nextgis_updater')
silent_install_dir_replacestr = silent_install_dir
if sys.platform == 'win32':
    silent_install_dir_replacestr = silent_install_dir.replace("\\", "\\\\")

script_content = """
function Controller() {
    installer.autoRejectMessageBoxes();
    installer.installationFinished.connect(function() {
        gui.clickButton(buttons.NextButton);
    })
}

Controller.prototype.WelcomePageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.CredentialsPageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.IntroductionPageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.TargetDirectoryPageCallback = function()
{
    gui.currentPageWidget().TargetDirectoryLineEdit.setText("install_path");
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.ComponentSelectionPageCallback = function() {
    var widget = gui.currentPageWidget();

    widget.deselectAll();
    widget.selectComponent("com.nextgis.utils.sqlite");
    // widget.deselectComponent("qt.tools.examples");

    gui.clickButton(buttons.NextButton);
}

Controller.prototype.LicenseAgreementPageCallback = function() {
    gui.currentPageWidget().AcceptLicenseRadioButton.setChecked(true);
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.StartMenuDirectoryPageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.ReadyForInstallationPageCallback = function() {
    gui.clickButton(buttons.NextButton);
}

Controller.prototype.FinishedPageCallback = function() {
    gui.clickButton(buttons.FinishButton);
}
        """.replace('install_path', silent_install_dir_replacestr)
script_path = os.path.join(tmp_dir, 'install.qs')
with open(script_path, "w") as text_file:
    text_file.write(script_content)

run((installer_exe, '--script', script_path))

# 3 Get installer files
color_print('Create updater package', False, 'LBLUE')
# 4 Pack nextgisupdater files to zip
pack_zip = os.path.join(tmp_dir, 'package.zip')
os.chdir(tmp_dir)
cmd = ('cmake', '-E', 'tar', 'cfv', pack_zip, '--format=zip')
cmd = cmd + (os.path.join(silent_install_dir, 'nextgisupdater.ini'), os.path.join(silent_install_dir, 'nextgisupdater.dat'),)
if sys.platform == 'darwin':
    cmd = cmd + (os.path.join(silent_install_dir, 'nextgisupdater.app'),)
else:
    cmd = cmd + (os.path.join(silent_install_dir, 'nextgisupdater.exe'),)
run(cmd)

# 5 Add version.str. Create version.str with increment version
ver_str = os.path.join(tmp_dir, 'version.str')
with open(ver_str, "w") as text_file:
    import datetime
    now = datetime.datetime.now()
    # get qtifw version
    component_name = 'com.nextgis.nextgis_updater'
    version_file_date = now.strftime("%Y-%m-%d %H:%M:%S")
    version_str = args.version
    version_str = version_str.replace("\'", "")
    version_str = version_str.replace("\"", "")
    text_file.write('{}\n{}\npackage'.format(version_str, version_file_date))

# 6 Send to ftp
ftp = args.ftpout
if ftp[-1:] != '/':
    ftp += '/'
ftp = ftp + 'src/' + updater_repo + '_' + suffix + '/'

run(('curl', '-u', args.ftpout_user, '-T', "{package.zip,version.str}", '-s', '--ftp-create-dirs', ftp))
