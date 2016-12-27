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
import pickle

args = {}

# ['lib_jsonc' = ['date': '1900-01-01 00:00:00', 'count': 1]]
libraries_version_dict = {}

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
packages_data_source_path = ''

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

    parser = argparse.ArgumentParser(description='Create NextGIS desktop software installer.', usage='%(prog)s [options]')
    parser.add_argument('-q', dest='qt_bin', required=True, help='QT bin path (path to lrelease)')
    parser.add_argument('-t', dest='target', required=True, help='target path')
    parser.add_argument('-s', dest='source', required=True, help='Packages data source path (i.e. borsch root directory)')
    parser.add_argument('-r', dest='remote', required=False, help='repositry remote url')
    parser.add_argument('-n', dest='network', action='store_true', help='online installer, the -r key should be present)')
    args = parser.parse_args()

def run(args):
    print 'calling ' + string.join(args)
    subprocess.check_call(args)

def load_versions():
    if os.path.exists('versions.pkl'):
        global libraries_version_dict
        with open('versions.pkl', 'rb') as f:
            libraries_version_dict = pickle.load(f)

def save_versions():
    with open('versions.pkl', 'wb') as f:
        pickle.dump(libraries_version_dict, f, pickle.HIGHEST_PROTOCOL)

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
    global packages_data_source_path

    load_versions()

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

    packages_data_source_path = os.path.abspath(args.source)
    if not os.path.exists(packages_data_source_path):
        sys.exit('Invalid packages data source path')

def get_repository_path():
    out_path = os.path.join(repo_target_path, 'repository')
    if sys.platform == 'darwin':
        out_path += '-mac'
    elif sys.platform == 'win32':
        out_path += '-win'
    else: # This should never happened
        out_path += '-nix'
    return out_path

def prepare_config():
    os.makedirs(repo_new_config_path)
    tree = ET.parse(os.path.join(repo_config_path, 'config.xml'))
    root = tree.getroot()

    installer_tag = root
    banner_tag = installer_tag.find('Banner')
    shutil.copy(os.path.join(repo_root_dir, 'art', banner_tag.text), repo_new_config_path)

    inst_app_icon_tag = installer_tag.find('InstallerApplicationIcon')
    inst_app_icon_path = os.path.join(repo_root_dir, 'art', inst_app_icon_tag.text)
    if sys.platform == 'darwin':
        inst_app_icon_tag.text += '.icns'
        inst_app_icon_path += '.icns'
    elif sys.platform == 'win32':
        inst_app_icon_tag.text += '.ico'
        inst_app_icon_path += '.ico'
    else:
        inst_app_icon_tag.text += '.png'
        inst_app_icon_path += '.png'

    shutil.copy(inst_app_icon_path, repo_new_config_path)

    inst_wnd_icon_tag = installer_tag.find('InstallerWindowIcon')
    shutil.copy(os.path.join(repo_root_dir, 'art', inst_wnd_icon_tag.text), repo_new_config_path)
    url_tag = installer_tag.find('RemoteRepositories/Repository/Url')
    if args.network:
        url_tag.text = repo_remote_path
    else:
        url_tag.text = 'file://' + get_repository_path()

    wizard_tag = installer_tag.find('WizardStyle')
    targetdir_tag = installer_tag.find('TargetDir')
    if sys.platform == 'darwin':
        wizard_tag.text = 'Modern'#'Mac'
    #    targetdir_tag = '@RootDir@' <-- root dir is forbidden as it will be deleted on reinstall
    else:
        wizard_tag.text = 'Modern'
    targetdir_tag.text = '@ApplicationsDir@/NextGIS'

    tree.write(os.path.join(repo_new_config_path, 'config.xml'))
    shutil.copy(os.path.join(repo_config_path, 'initscript.qs'), repo_new_config_path)

def copyFiles(tag, sources_root_dir, data_path):
    for path in tag.iter('path'):
        src_path = path.attrib['src']
        dst_path = path.attrib['dst']
        shutil.copytree(os.path.join(sources_root_dir, src_path), os.path.join(data_path, dst_path))
    return

def get_version_text(sources_root_dir):
    version_file_path = os.path.join(packages_data_source_path, sources_root_dir, 'build', 'version.str')
    with open(version_file_path) as f:
        content = f.readlines()
        version_str = content[0].rstrip()
        version_file_date = content[1].rstrip()

    if sources_root_dir in libraries_version_dict:
        if libraries_version_dict[sources_root_dir]['version'] == version_str:
            if libraries_version_dict[sources_root_dir]['date'] == version_file_date:
                version_str += '-' + str(libraries_version_dict[sources_root_dir]['count'])
            else:
                count = libraries_version_dict[sources_root_dir]['count'] + 1
                version_str += '-' + str(count)
                libraries_version_dict[sources_root_dir]['count'] = count
                libraries_version_dict[sources_root_dir]['date'] = version_file_date
        else:
            libraries_version_dict[sources_root_dir]['count'] = 0
            libraries_version_dict[sources_root_dir]['date'] = version_file_date
            libraries_version_dict[sources_root_dir]['version'] = version_str
            version_str += '-0'
    else:
        libraries_version_dict[sources_root_dir] = dict(count = 0, date = version_file_date, version = version_str)
        version_str += '-0'

    return version_str

def process_directory(dir_name):
    color_print('Process ' + dir_name, True, 'LBLUE')
    path = os.path.join(repo_source_path, dir_name)
    path_meta = os.path.join(path, 'meta')
    path_data = os.path.join(path, 'data')

    if not os.path.exists(path_data):
        return

    # Parse install.xml file
    if not os.path.exists(os.path.join(path_data, 'package.xml')):
        return

    tree = ET.parse(os.path.join(path_data, 'package.xml'))
    root = tree.getroot()

    if 'root' in root.attrib:
        sources_root_dir = root.attrib['root']
        version_text = get_version_text(sources_root_dir)
    else:
        version_text = root.find('Version').text

    updatetext_tag = root.find('UpdateText')
    updatetext_text = None
    if updatetext_tag is not None:
        updatetext_text = updatetext_tag.text

    # Copy files
    repo_new_package_path = os.path.join(repo_new_packages_path, dir_name)
    os.makedirs(repo_new_package_path)
    new_data_path = os.path.join(repo_new_package_path, 'data')
    if sys.platform == 'darwin':
        mac_tag = root.find('mac')
        if mac_tag is not None:
            copyFiles(mac_tag, os.path.join(packages_data_source_path, sources_root_dir), new_data_path)
    elif sys.platform == 'win32':
        win_tag = root.find('win')
        if win_tag is not None:
            copyFiles(win_tag, os.path.join(packages_data_source_path, sources_root_dir), new_data_path)

    # Process package.xml
    tree = ET.parse(os.path.join(path_meta, 'package.xml'))
    root = tree.getroot()
    releasedate_tag = root.find('ReleaseDate')
    if releasedate_tag is None:
        releasedate_tag = ET.SubElement(root, 'ReleaseDate')
    releasedate_tag.text = time.strftime("%Y-%m-%d")
    name_tag = root.find('Name')
    if name_tag is None:
        name_tag = ET.SubElement(root, 'Name')
    name_tag.text = dir_name
    version_tag = root.find('Version')
    if version_tag is None:
        version_tag = ET.SubElement(root, 'Version')
    version_tag.text = version_text
    if updatetext_text is not None:
        updatetext_tag = root.find('UpdateText')
        if updatetext_tag is None:
            updatetext_tag = ET.SubElement(root, 'UpdateText')
        updatetext_tag.text = updatetext_text

    # TODO: Additional change to xml
    new_meta_path = os.path.join(repo_new_package_path, 'meta')
    os.makedirs(new_meta_path)
    tree.write(os.path.join(new_meta_path, 'package.xml'))

    for meta_file in os.listdir(path_meta):
        if meta_file == 'package.xml':
            continue

        meta_file_path = os.path.join(path_meta, meta_file)
        filename, file_extension = os.path.splitext(os.path.basename(meta_file_path))
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
        shutil.rmtree(repo_target_path, ignore_errors=True)
    if os.path.exists(repo_target_path):
        print 'delete existing build dir ...'
        shutil.rmtree(repo_target_path, ignore_errors=True)
    os.makedirs(repo_target_path)

    prepare_config()
    prepare_packages()

def create_installer():
    run((repogen_file, '--remove', '-v', '-p', repo_new_packages_path, get_repository_path()))
    key_only = '--offline-only'
    if args.network:
        key_only = '--online-only'
    run((binarycreator_file, '-v', key_only, '-c', os.path.join(repo_new_config_path, 'config.xml'), '-p', repo_new_packages_path, os.path.join(repo_target_path, 'nextgis-setup') ))

    # Hack as <InstallerApplicationIcon> in config.xml not working
    if sys.platform == 'darwin':
        icns_path = os.path.join(repo_target_path, 'nextgis-setup.app', 'Contents', 'Resources', 'nextgis-setup.icns' )
        os.unlink(icns_path)
        shutil.copy(os.path.join(repo_new_config_path, 'nextgis-setup.icns'), icns_path)

    print 'DONE, installer is at ' + os.path.join(repo_target_path, 'nextgis-setup')


parse_arguments()
init()
prepare()
create_installer()
save_versions()
