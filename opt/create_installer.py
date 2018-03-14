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

import argparse
import os
import shutil
import string
import subprocess
import sys
import xml.etree.ElementTree as ET
import time
import pickle
import glob

args = {}
libraries_version_dict = {}

repogen_file = ''
binarycreator_file = ''
versions_file_name = ''
repo_config_path = ''
repo_target_path = ''
repo_source_path = ''
repo_remote_path = ''
repo_root_dir = ''
repo_new_packages_path = ''
repo_new_config_path = ''
translate_tool = ''
packages_data_source_path = ''
mac_sign_identy = "Developer ID Application: NextGIS OOO (A65C694QW9)"

repositories = ['lib_z', 'lib_openssl', 'lib_curl', 'lib_sqlite', 'lib_gif',
                'lib_qhull', 'lib_png', 'lib_freetype', 'lib_agg', 'lib_geos',
                'lib_expat', 'lib_jsonc', 'lib_opencad', 'lib_jpeg', 'lib_pq',
                'lib_proj', 'lib_lzma', 'lib_jbig', 'lib_szip', 'lib_xml2',
                'lib_spatialite', 'lib_openjpeg', 'lib_tiff', 'lib_geotiff',
                'lib_hdf4', 'lib_gsl', 'lib_yaml', 'py_yaml', 'numpy', 'lib_gdal',
                ]

repositories_win = ['lib_iconv', 'python',
                ]

repositories_not_stored = ['py_exifread', 'py_functools_lru_cache',
                            'py_cycler', 'py_parsing', 'py_contextlib',
                            'py_raven', 'py_future', 'py_requests', 'py_pytz',
                            'py_nose', 'py_jinja', 'py_httplib', 'py_ows', 'py_dateutil',
                            'py_pygments', 'py_six',
                        ]

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

    parser = argparse.ArgumentParser(description='Create NextGIS desktop software installer.')
    parser.add_argument('-q', dest='qt_bin', required=True, help='Qt binary path (path to lrelease)')
    parser.add_argument('-t', dest='target', required=True, help='Target path')
    parser.add_argument('-s', dest='source', required=True, help='Relative path from current working directory (CWD) to packages data source  (i.e. borsch root directory)')
    parser.add_argument('-se', dest='source_ext', required=False, help='Extended packages data source path (i.e. qgis directory)')
    parser.add_argument('-r', dest='remote', required=False, help='Repositry remote url')
    parser.add_argument('-n', dest='network', action='store_true', help='Online installer (the -r key should be present)')
    parser.add_argument('-i', dest='installer_name', required=False, help='Installer name')
    if sys.platform == 'win32':
        parser.add_argument('-w64', dest='win64', action='store_true', help='Flag to build Windows 64bit repository')
        parser.add_argument('-g', dest='generator', required=False, help='Visual Studio generator')

    subparsers = parser.add_subparsers(help='command help', dest='command')
    parser_prepare = subparsers.add_parser('prepare')
    parser_prepare.add_argument('--ftp_user', dest='ftp_user', required=False, help='FTP user name and password to fetch package.zip anv version.str files')
    parser_prepare.add_argument('--ftp', dest='ftp', required=False, help='FTP address with directories to fetch package.zip anv version.str files')

    parser_create = subparsers.add_parser('create')

    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('--force', dest='packages', required=False, nargs='+', help='Force update specified packages even not any changes exists. If all specified force update all packages')
    args = parser.parse_args()


def run(args):
    print 'calling ' + string.join(args)
    subprocess.check_call(args)

def run_shell(args):
    print 'calling ' + args
    # subprocess.check_call(args, shell=True)

    p = subprocess.Popen(args, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    rc = p.returncode

    print 'o: ' + output
    print 'e: ' + err

    if rc != 0:
        sys.exit('Failed to call')


def load_versions(file_name):
    color_print('load versions from ' + file_name, True, 'LYELLOW')
    if os.path.exists(file_name):
        global libraries_version_dict
        with open(file_name, 'rb') as f:
            libraries_version_dict = pickle.load(f)


def save_versions(file_name):
    color_print('save versions to ' + file_name, True, 'LGREEN')
    with open(file_name, 'wb') as f:
        pickle.dump(libraries_version_dict, f, pickle.HIGHEST_PROTOCOL)


def init():
    color_print('Initializing ...', True, 'LYELLOW')
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
    global versions_file_name
    global repo_remote_path

    repo_root_dir = os.path.dirname(os.path.abspath(os.path.dirname(sys.argv[0])))

    bin_dir = os.path.join(repo_root_dir, 'qtifw_pkg', 'bin')
    repogen_file = os.path.join(bin_dir, 'repogen')
    color_print('repogen path: ' + repogen_file, True, 'LCYAN')
    binarycreator_file = os.path.join(bin_dir, 'binarycreator')
    color_print('binarycreator path: ' + binarycreator_file, True, 'LCYAN')
    scripts_path = os.path.join(repo_root_dir, 'qtifw_scripts')
    repo_config_path = os.path.join(scripts_path, 'config')
    repo_source_path = os.path.join(scripts_path, 'packages')
    repo_target_path = os.path.abspath(args.target)

    color_print('build path: ' + repo_target_path, True, 'LCYAN')
    repo_new_packages_path = os.path.join(repo_target_path, 'packages')
    repo_new_config_path = os.path.join(repo_target_path, 'config')

    if args.network:
        repo_remote_path = args.remote
        print 'remote repository URL: ' + repo_remote_path

    translate_tool = os.path.join(args.qt_bin, 'lrelease')
    if sys.platform == 'win32':
        translate_tool += '.exe'

    is_releative = False

    if not os.path.exists(translate_tool):
        translate_tool = os.path.join(repo_root_dir, translate_tool)
        is_releative = True
        if not os.path.exists(translate_tool):
            sys.exit('No translate tool exists')

    translate_tool = os.path.abspath(translate_tool)
    color_print('lrelease path: ' + translate_tool, True, 'LCYAN')

    if is_releative:
        packages_data_source_path = os.path.join(repo_root_dir, args.source)
    else:
        packages_data_source_path = os.path.abspath(args.source)


    color_print('packages path: ' + packages_data_source_path, True, 'LCYAN')

    versions_file_name = os.path.join(repo_root_dir, 'versions.pkl')
    load_versions(versions_file_name)

def get_sources_dir_path(sources_root_dir):
    if args.source_ext:
        sources_dir_path = os.path.join(args.source_ext, sources_root_dir)
        if os.path.exists(sources_dir_path):
            return sources_dir_path

    return os.path.join(packages_data_source_path, sources_root_dir)

def get_repository_path():
    if repo_remote_path != '':
        out_path = os.path.join(repo_target_path, os.path.basename(repo_remote_path))
    else:
        out_path = os.path.join(repo_target_path, 'repository')
        if sys.platform == 'darwin':
            out_path += '-mac'
        elif sys.platform == 'win32':
            if args.win64:
                out_path += '-win64'
            else:
                out_path += '-win32'
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
        shutil.copy(os.path.join(repo_root_dir, 'art', 'bk.png'), repo_new_config_path)
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
        src_path_full = unicode(os.path.join(sources_root_dir, src_path))
        dst_path_full = unicode(os.path.join(data_path, dst_path))

        if os.path.islink(src_path_full):
            linkto = os.readlink(src_path_full)
            parent_dir = os.path.dirname(dst_path_full)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
            os.symlink(linkto, dst_path_full)
        else:
            if os.path.isdir(src_path_full):
                shutil.copytree(src_path_full, dst_path_full, symlinks=True)
            else:
                if not os.path.exists(dst_path_full):
                    os.makedirs(dst_path_full)

                if src_path_full.find('*'):
                    # Copy by wildcard.
                    for copy_file in glob.glob(src_path_full):
                        shutil.copy(copy_file, dst_path_full)
                else:
                    if os.path.exists(src_path_full):
                        shutil.copy(src_path_full, dst_path_full)
    return


def check_version(version_str, version_file_date, component_name, force):
    has_changes = False
    if component_name in libraries_version_dict:
        if libraries_version_dict[component_name]['version'] == version_str:
            if libraries_version_dict[component_name]['date'] == version_file_date and force == False:
                version_str += '-' + str(libraries_version_dict[component_name]['count'])
            else:
                count = libraries_version_dict[component_name]['count'] + 1
                version_str += '-' + str(count)
                libraries_version_dict[component_name]['count'] = count
                libraries_version_dict[component_name]['date'] = version_file_date
                has_changes = True
        else:
            libraries_version_dict[component_name]['count'] = 0
            libraries_version_dict[component_name]['date'] = version_file_date
            libraries_version_dict[component_name]['version'] = version_str
            version_str += '-0'
            has_changes = True
    else:
        libraries_version_dict[component_name] = dict(count = 0, date = version_file_date, version = version_str)
        version_str += '-0'
        has_changes = True

    return version_str, has_changes


def get_version_text(sources_root_dir, component_name, force):
    has_changes = False
    version_file_path = os.path.join(get_sources_dir_path(sources_root_dir), 'version.str')
    if not os.path.exists(version_file_path):
        version_file_path = os.path.join(get_sources_dir_path(sources_root_dir), 'build', 'version.str')
        if not os.path.exists(version_file_path):
            return "0.0.0", has_changes

    with open(version_file_path) as f:
        content = f.readlines()
        version_str = content[0].rstrip()
        version_file_date = content[1].rstrip()

    return check_version(version_str, version_file_date, component_name, force)


def process_files_in_meta_dir(path_meta, new_meta_path):
    if not os.path.exists(new_meta_path):
        return
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


def create_dest_package_dir(dir_name, version_text, updatetext_text, sources_dir, repo_new_package_path, data_root_tag, path_meta):

    # If not install under current system - don't create directory
    is_dir_maked = False
    new_data_path = os.path.join(repo_new_package_path, 'data')
    if sys.platform == 'darwin':
        mac_tag = data_root_tag.find('mac')
        if mac_tag is not None:
            if not is_dir_maked:
                is_dir_maked = True
                os.makedirs(repo_new_package_path)
            copyFiles(mac_tag, sources_dir, new_data_path)
        else:
            if data_root_tag.find('Version') is None:
                return
    elif sys.platform == 'win32':
        win_tag = data_root_tag.find('win')
        if win_tag is not None:
            if not is_dir_maked:
                is_dir_maked = True
                os.makedirs(repo_new_package_path)
            copyFiles(win_tag, sources_dir, new_data_path)
        else:
            if data_root_tag.find('Version') is None:
                return

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

    dependencies_tag = root.find('Dependencies')
    if dependencies_tag is not None:
        # If Mac OS X
        if sys.platform == 'darwin':
            dependencies_tag.text = dependencies_tag.text.replace('com.nextgis.common.qt.all,', '') # Only install qt.conf which installed in separate app folder on Mac OS X
            dependencies_tag.text = dependencies_tag.text.replace('com.nextgis.common.qt.all', '')
            dependencies_tag.text = dependencies_tag.text.replace('com.nextgis.python.python,', '') # Python 2 is default application in Mac OS X
            dependencies_tag.text = dependencies_tag.text.replace('com.nextgis.python.python', '')
            dependencies_tag.text = dependencies_tag.text.replace('com.nextgis.common.vc,', '')
            dependencies_tag.text = dependencies_tag.text.replace('com.nextgis.common.vc', '')


        dependencies_tag.text = dependencies_tag.text.replace('  ', ' ')
        dependencies_tag.text = dependencies_tag.text.replace(', ', ',')
        if dependencies_tag.text.endswith(','):
            dependencies_tag.text = dependencies_tag.text[:-1]

    new_meta_path = os.path.join(repo_new_package_path, 'meta')
    os.makedirs(new_meta_path)
    tree.write(os.path.join(new_meta_path, 'package.xml'))
    process_files_in_meta_dir(path_meta, new_meta_path)


def process_directory(dir_name):
    color_print('Process ' + dir_name, True, 'LBLUE')
    path = os.path.join(repo_source_path, dir_name)
    path_meta = os.path.join(path, 'meta')
    path_data = os.path.join(path, 'data')

    if not os.path.exists(path_data):
        return

    package_xml = os.path.join(path_data, 'package.xml')
    # Parse package.xml file
    if not os.path.exists(package_xml):
        return

    tree = ET.parse(package_xml)
    root = tree.getroot()

    sources_root_dir = ''
    if 'root' in root.attrib:
        sources_root_dir = root.attrib['root']
        version_text, has_changes = get_version_text(sources_root_dir, dir_name, False)
    else:
        mtime = time.gmtime(os.path.getmtime(package_xml))
        version_date = time.strftime('%Y-%m-%d %H:%M:%S', mtime)
        version_text, has_changes = check_version(root.find('Version').text, version_date, dir_name, False)

    updatetext_tag = root.find('UpdateText')
    updatetext_text = None
    if updatetext_tag is not None:
        updatetext_text = updatetext_tag.text

    # Avoid creating package if disabled. Temporary only for Windows.
    if sys.platform == 'win32':
        tag_os = root.find('win')
        if tag_os is not None:
            attr_enabled = tag_os.get('enabled')
            if attr_enabled is not None and attr_enabled == 'false':
                color_print('... not add because package data config has not enabled attr in <win> tag', True, 'LBLUE')
                return
    repo_new_package_path = os.path.join(repo_new_packages_path, dir_name)
    create_dest_package_dir(dir_name, version_text, updatetext_text, get_sources_dir_path(sources_root_dir), repo_new_package_path, root, path_meta)
    color_print('... added as a package', True, 'LBLUE')


def prepare_packages():
    os.makedirs(repo_new_packages_path)

    # Scan for directories and files
    for subdir in os.listdir(repo_source_path):
        if os.path.isdir(os.path.join(repo_source_path, subdir)):
            process_directory(subdir)

def prepare_win_redist(target_dir):
    color_print('Create Microsoft Visual C++ Redistributable Packages', True, 'LCYAN')
    generator = args.generator

    # Create build/inst directory for vc_redist
    target_repo_dir = os.path.join(target_dir, 'vc_redist')
    target_repo_build_dir = os.path.join(target_repo_dir, 'build')
    if not os.path.exists(target_repo_build_dir):
        os.makedirs(target_repo_build_dir)

    # Copy CMakeLists to this dir
    src_cmake = os.path.join(repo_root_dir, 'opt', 'CMakeLists.txt')
    shutil.copy(src_cmake, target_repo_dir)

    # Build and Install
    os.chdir( target_repo_build_dir )
    run(('cmake', '-DCMAKE_BUILD_TYPE=Release', '-DSKIP_DEFAULTS=ON', '-DCMAKE_INSTALL_PREFIX=' + os.path.join(target_repo_dir,'inst'), '-G', generator, '..'))
    run(('cmake', '--build', '.', '--config', 'Release', '--target', 'install'))

def delete_path(path_to_delete):
    color_print('Delete existing build dir ...', True, 'LRED')
    shutil.rmtree(path_to_delete, ignore_errors=True)

def download(ftp_user, ftp, target_dir):
    if ftp is None:
        return

    tmp_dir = os.path.join(os.getcwd(), 'tmp')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    target_dir = os.path.join(os.getcwd(), target_dir)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    data_dir = os.path.join(repo_root_dir, 'data')
    for f in os.listdir(data_dir):
        copy_dir = os.path.join(data_dir, f)
        if os.path.isdir(copy_dir):
            color_print('Process ' + f, True, 'LGREEN')
            shutil.copytree(copy_dir, os.path.join(target_dir, f), symlinks=True)

    if sys.platform == 'win32':
        prepare_win_redist(target_dir)

    # Download and install not compile repositories (i.e. py)
    for repository in repositories_not_stored:
        color_print('Process ' + repository, True, 'LGREEN')
        target_repo_dir = os.path.join(target_dir, repository)
        run(('git', 'clone', '--depth', '1', 'git://github.com/nextgis-borsch/{}.git'.format(repository), os.path.join(target_dir, repository) ))
        build_dir = os.path.join(target_repo_dir, 'build')
        os.makedirs(build_dir)
        os.chdir( build_dir )
        run(('cmake', '-DCMAKE_BUILD_TYPE=Release', '-DSKIP_DEFAULTS=ON', '-DCMAKE_INSTALL_PREFIX=' + os.path.join(target_repo_dir,'inst'), '..'))
        run(('cmake', '--build', '.', '--config', 'Release'))
        run(('cmake', '--build', '.', '--config', 'Release', '--target', 'install'))

    suffix = 'nix'
    if sys.platform == 'darwin':
        suffix = 'mac'
    elif sys.platform == 'win32':
        if args.win64:
            suffix = 'win64'
        else:
            suffix = 'win32'

    os.chdir( tmp_dir )

    # Download and install already compiled repositories (i.e. lib)
    # 1. Get archive to tmp directory

    if sys.platform == 'win32':
        repositories.extend(repositories_win)

    for repository in repositories:
        color_print('Download ' + repository + '_' + suffix, True, 'LGREEN')
        ftp_dir = repository + '_' + suffix
        if ftp[-1:] != '/':
            ftp += '/'
        out_zip = os.path.join(tmp_dir, 'package.zip')
        run(('curl', '-u', ftp_user, ftp + ftp_dir + '/package.zip', '-o', out_zip, '-s'))

# 2. Extract archive
        color_print('Extract ' + out_zip, False, 'LGREEN')
        run(('cmake', '-E', 'tar', 'xzf', out_zip))

# 3. Move archive with new name to target_dir
        target_repo_dir = os.path.join(target_dir, repository)
        for o in os.listdir(tmp_dir):
            archive_dir = os.path.join(tmp_dir,o)
            if os.path.isdir(archive_dir):
                shutil.move(archive_dir, target_repo_dir)
                break

# 4. Download version.str
        if os.path.exists(target_repo_dir):
            color_print('Download ' + repository + '_' + suffix + '/version.str', True, 'LGREEN')
            run(('curl', '-u', ftp_user, ftp + ftp_dir + '/version.str', '-o', os.path.join(target_repo_dir, 'version.str'), '-s'))

def prepare():
    color_print('Preparing ...', True, 'LYELLOW')

    if os.path.exists(repo_target_path):
        delete_path(repo_target_path)
    if os.path.exists(repo_target_path):
        delete_path(repo_target_path)
    os.makedirs(repo_target_path)

    prepare_config()
    prepare_packages()


def update_directory(dir_name, force):
    color_print('Update ' + dir_name, True, 'LBLUE')
    path = os.path.join(repo_source_path, dir_name)
    path_meta = os.path.join(path, 'meta')
    path_data = os.path.join(path, 'data')

    if not os.path.exists(path_data):
        return

    package_xml = os.path.join(path_data, 'package.xml')
    # Check versions, if differ - delete directory and load it from sources.
    if not os.path.exists(package_xml):
        return

    tree = ET.parse(package_xml)
    root = tree.getroot()

    sources_root_dir = ''
    if 'root' in root.attrib:
        sources_root_dir = root.attrib['root']
        version_text, has_changes = get_version_text(sources_root_dir, dir_name, force)
    else:
        mtime = time.gmtime(os.path.getmtime(package_xml))
        version_date = time.strftime('%Y-%m-%d %H:%M:%S', mtime)
        version_text, has_changes = check_version(root.find('Version').text, version_date, dir_name, force)

    repo_new_package_path = os.path.join(repo_new_packages_path, dir_name)
    if not has_changes:
        # Update translations
        new_meta_path = os.path.join(repo_new_package_path, 'meta')
        process_files_in_meta_dir(path_meta, new_meta_path)
        color_print('No changes in ' + dir_name, True, 'LCYAN')
        return

    updatetext_tag = root.find('UpdateText')
    updatetext_text = None
    if updatetext_tag is not None:
        updatetext_text = updatetext_tag.text

    if os.path.exists(repo_new_package_path):
        color_print('Delete existing dir ' + repo_new_package_path, True, 'LRED')
        shutil.rmtree(repo_new_package_path, ignore_errors=True)

    # Avoid creating package if disabled. Temporary only for Windows.
    if sys.platform == 'win32':
        tag_os = root.find('win')
        if tag_os is not None:
            attr_enabled = tag_os.get('enabled')
            if attr_enabled is not None and attr_enabled == 'false':
                return
    create_dest_package_dir(dir_name, version_text, updatetext_text, get_sources_dir_path(sources_root_dir), repo_new_package_path, root, path_meta)
    color_print('... package updated', True, 'LBLUE')


def update(packages):
    force_all = False
    if packages:
        if 'all' in packages:
            force_all = True
            packages = []
            source_dirs = os.listdir(repo_source_path)
        else:
            source_dirs = packages
    else:
        # Scan for directories and files
        packages = []
        source_dirs = os.listdir(repo_source_path)

    for subdir in source_dirs:
        if os.path.isdir(os.path.join(repo_source_path, subdir)):
            update_directory(subdir, len(packages) > 0 or force_all)
    if not packages:
        # Delete not exist directories for full repo update
        for subdir in os.listdir(repo_new_packages_path):
            if not subdir in source_dirs:
                delete_path(os.path.join(repo_source_path, subdir))


def create_installer():
    run((repogen_file, '--remove', '-v', '-p', repo_new_packages_path, get_repository_path()))
    key_only = '--offline-only'
    if args.network:
        key_only = '--online-only'

    installer_name = 'nextgis-setup'
    if args.installer_name:
        installer_name = args.installer_name

    # Hack as <InstallerApplicationIcon> in config.xml not working
    if sys.platform == 'darwin':
        run((binarycreator_file, '-v', key_only, '-c', os.path.join(repo_new_config_path, 'config.xml'), '-p', repo_new_packages_path, os.path.join(repo_target_path, 'nextgis-setup'), '--sign', mac_sign_identy))

        import dmgbuild
        icns_path = os.path.join(repo_target_path, 'nextgis-setup.app', 'Contents', 'Resources', 'nextgis-setup.icns' )
        os.unlink(icns_path)
        shutil.copy(os.path.join(repo_new_config_path, 'nextgis-setup.icns'), icns_path)

        # Resign install application as there is some bug in binarycreator --sign
        # run_shell('codesign --deep --force --verify --verbose --sign \"{}\" {}'.format(mac_sign_identy, os.path.join(repo_target_path, 'nextgis-setup.app')))

        run(('codesign', '--deep', '--force',  '--verify', '--verbose', '--sign', mac_sign_identy, os.path.join(repo_target_path, 'nextgis-setup.app') ))

        # Build dgm image file
        color_print('Create DMG file ...', True, 'LMAGENTA')
        dmgbuild.build_dmg(
            os.path.join(repo_target_path, installer_name + '.dmg'),
            'NextGIS Setup',
            os.path.join(repo_root_dir, 'opt', 'dmg_settings.py'),
            defines=dict(badge_icon=os.path.join(repo_new_config_path, 'nextgis-setup.icns'),
                 background=os.path.join(repo_new_config_path, 'bk.png'),
                 files=[os.path.join(repo_target_path, 'nextgis-setup.app')]),
            lookForHiDPI=False)
    else:
        run((binarycreator_file, '-v', key_only, '-c', os.path.join(repo_new_config_path, 'config.xml'), '-p', repo_new_packages_path, os.path.join(repo_target_path, installer_name) ))

    color_print('DONE, installer is at ' + os.path.join(repo_target_path, installer_name), True, 'LMAGENTA')


def update_istaller():
    run((repogen_file, '--update-new-components', '-v', '-p', repo_new_packages_path, get_repository_path()))
    color_print('DONE, installer is at ' + os.path.join(repo_target_path, 'nextgis-setup'), True, 'LMAGENTA')


parse_arguments()
init()
if args.command == 'create':
    prepare()
    create_installer()
elif args.command == 'prepare':
    download(args.ftp_user, args.ftp, args.source)
    prepare()
elif args.command == 'update':
    packages = []
    if args.packages:
        if len(args.packages) == 1:
            packages = args.packages[0].split()
        else:
            packages = args.packages
    else:
        packages = None
    update(packages)
    update_istaller()
else:
    exit('Unsupported command')
save_versions(versions_file_name)
