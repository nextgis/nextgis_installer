#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
##
## Project: NextGIS online/offline installer
## Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
## Copyright (c) 2016 NextGIS <info@nextgis.com>
## License: GPL v.2
##
################################################################################

import argparse
import os
import shutil
import string
import subprocess
import sys
import xml.etree.ElementTree as ET
import time

args = {}

repogen_file = ''
binarycreator_file = ''

repo_config_path = ''
repo_target_path = ''
repo_source_path = ''
repo_remote_path = ''
repo_root_dir = ''
repo_new_packages_path = ''
repo_new_config_path = ''
translate_tool = ''

def parse_arguments():
    global args

    parser = argparse.ArgumentParser(description='Create NextGIS desktop software installer.', usage='%(prog)s [options]')
    parser.add_argument('-q', dest='qt_bin', required=True, help='QT bin path (path to lrelease)')
    parser.add_argument('-t', dest='target', required=True, help='target path')
    parser.add_argument('-r', dest='remote', required=False, help='repositry remote url')
    parser.add_argument('-n', dest='network', action='store_true', help='online installer, the -r key should be present)')
    args = parser.parse_args()

def run(args):
    print 'calling ' + string.join(args)
    subprocess.check_call(args)

def init():
    print 'Initializing ...'
    global repogen_file
    global binarycreator_file
    global repo_config_path
    global repo_source_path
    global repo_target_path
    global repo_new_packages_path
    global repo_root_dir
    global repo_new_config_path
    global translate_tool

    repo_root_dir = os.path.dirname(os.path.abspath(os.path.dirname(sys.argv[0])))

    bin_dir = os.path.join(repo_root_dir, 'qtifw_pkg', 'bin')
    repogen_file = os.path.join(bin_dir, 'repogen')
    print 'repogent path: ' + repogen_file
    binarycreator_file = os.path.join(bin_dir, 'binarycreator')
    print 'binarycreator path: ' + binarycreator_file
    scripts_path = os.path.join(repo_root_dir, 'qtifw_scripts')
    repo_config_path = os.path.join(scripts_path, 'config')
    repo_source_path = os.path.join(scripts_path, 'packages')
    repo_target_path = os.path.abspath(args.target)
    print 'build path: ' + repo_target_path
    repo_new_packages_path = os.path.join(repo_target_path, 'packages')
    repo_new_config_path = os.path.join(repo_target_path, 'config')

    if args.network:
        global repo_remote_path
        repo_remote_path = args.remote
        print 'remote repository URL: ' + repo_remote_path

    translate_tool = os.path.join(args.qt_bin, 'lrelease')
    if not os.path.exists(translate_tool):
        sys.exit('No translate tool exists')

def prepare_config():
    tree = ET.parse(os.path.join(repo_config_path, 'config.xml'))
    root = tree.getroot()

    installer_tag = root
    banner_tag = installer_tag.find('Banner')
    banner_tag.text = os.path.join(repo_root_dir, 'art', banner_tag.text)
    inst_app_icon_tag = installer_tag.find('InstallerApplicationIcon')
    inst_app_icon_tag.text = os.path.join(repo_root_dir, 'art', inst_app_icon_tag.text)
    if sys.platform == 'darwin':
        inst_app_icon_tag.text += '.icns'
    elif sys.platform == 'windows':
        inst_app_icon_tag.text += '.ico'
    else:
        inst_app_icon_tag.text += '.png'

    inst_wnd_icon_tag = installer_tag.find('InstallerWindowIcon')
    inst_wnd_icon_tag.text = os.path.join(repo_root_dir, 'art', inst_wnd_icon_tag.text)
    url_tag = installer_tag.find('RemoteRepositories/Repository/Url')
    if args.network:
        url_tag.text = repo_remote_path
    else:
        url_tag.text = 'file://' +  os.path.join(repo_target_path, 'repository')
    if sys.platform == 'darwin':
        url_tag.text += '-mac'
    elif sys.platform == 'windows':
        url_tag.text += '-win'
    else: # This should never happened
        url_tag.text += '-nix'

    wizard_tag = installer_tag.find('WizardStyle')
    targetdir_tag = installer_tag.find('TargetDir')
    if sys.platform == 'darwin':
        wizard_tag.text = 'Mac'
        targetdir_tag = '@RootDir@'
    else:
        wizard_tag.text = 'Modern'
        targetdir_tag = '@ApplicationsDir@/NextGIS'

    os.makedirs(repo_new_config_path)
    tree.write(os.path.join(repo_new_config_path, 'config.xml'))
    shutil.copy(os.path.join(repo_config_path, 'initscript.qs'), repo_new_config_path)

def copyFiles(tag):
    return

def process_directory(dir_name):
    path = os.path.join(repo_source_path, dir_name)
    path_meta = os.path.join(path, 'meta')
    path_data = os.path.join(path, 'data')

    if not os.path.exists(path_data):
        return

    # Parse install.xml file
    tree = ET.parse(os.path.join(path_data, 'package.xml'))
    root = tree.getroot()
    version_text = root.find('Version').text
    updatetext_tag = root.find('UpdateText')
    if updatetext_tag is not None:
        updatetext_text = updatetext_tag.text

    # Copy files
    if sys.platform == 'darwin':
        mac_tag = root.find('mac')
        if mac_tag is not None:
            copyFiles(mac_tag)
    elif sys.platform == 'windows':
        win_tag = root.find('win')
        if win_tag is not None:
            copyFiles(win_tag)

    # Process package.xml
    tree = ET.parse(os.path.join(path_meta, 'package.xml'))
    root = tree.getroot()
    releasedate_tag = root.find('ReleaseDate')
    if releasedate_tag is None:
        root.set('ReleaseDate', time.strftime("%Y-%m-%d"))
    else:
        releasedate_tag.text = time.strftime("%Y-%m-%d")
    name_tag = root.find('Name')
    if name_tag is None:
        root.set('Name', dir_name)
    else:
        name_tag.text = dir_name
    version_tag = root.find('Version')
    if version_tag is None:
        root.set('Version', version_text)
    else:
        version_tag.text = version_text
    if updatetext_text is not None:
        updatetext_tag = root.find('UpdateText')
        if updatetext_tag is None:
            root.set('UpdateText', version_text)
        else:
            updatetext_tag.text = updatetext_text

    # TODO: Additional change to xml
    repo_new_package_path = os.path.join(repo_new_packages_path, dir_name)
    os.makedirs(repo_new_package_path)
    new_meta_path = os.path.join(repo_new_package_path, 'meta')
    os.makedirs(new_meta_path)
    tree.write(os.path.join(new_meta_path, 'packages.xml'))

    for meta_file in os.listdir(path_meta):
        if meta_file == 'package.xml':
            continue

        meta_file_path = os.path.join(path_meta, meta_file)
        filename, file_extension = os.path.splitext(os.path.basename(meta_file_path))
        print 'meta_file -- ' + filename + '; ' + file_extension
        if file_extension == '.ts':
            # Create translation
            output_translation_path = os.path.join(new_meta_path, filename) + '.qm'
            run((translate_tool, meta_file_path, '-qm', output_translation_path))
        elif file_extension == '.qs':
            shutil.copy(meta_file_path, new_meta_path)


def prepare_packages():
    os.makedirs(repo_new_packages_path)

    # Scan for directories and files
    for subdir in os.listdir(repo_source_path):
        if os.path.isdir(os.path.join(repo_source_path, subdir)):
            process_directory(subdir)

def prepare():
    print 'Preparing ...'

    if os.path.exists(repo_target_path):
        print 'delete existing build dir ...'
        shutil.rmtree(repo_target_path)
    os.makedirs(repo_target_path)

    prepare_config()
    prepare_packages()


parse_arguments()
init()
prepare()

print 'DONE, installer is at ' + os.path.join(repo_target_path, 'nextgis-setup')
