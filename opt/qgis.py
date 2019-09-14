# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import sys
import os
from distutils.version import LooseVersion
import urllib
import subprocess
import tempfile

def run(args):
    subprocess.check_call(args)

def extract_value(text):
    return text.replace(")", "").strip()

def get_qgis_version():
    url = 'https://github.com/nextgis/nextgisqgis/blob/master/cmake/util.cmake'
    qgis_major = "0"
    qgis_minor = "0"
    u2 = urllib.urlopen(url)
    for line in u2.readlines():
        if "set(QGIS_MAJOR" in line:
            qgis_major = extract_value(line.replace("set(QGIS_MAJOR", ""))
        elif "set(QGIS_MINOR" in line:
            qgis_minor = extract_value(line.replace("set(QGIS_MINOR", ""))
    return '{}.{}'.format(qgis_major, qgis_minor)

def install_plugins(plugins_list, out_dir):

    qgis_version = get_qgis_version()

    metadata_xml_urls = [
        'http://plugins.qgis.org/plugins/plugins.xml?qgis=' + qgis_version,
        'https://rm.nextgis.com/api/repo/1/qgis_xml?qgis=' + qgis_version,
        # 'http://nextgis.ru/programs/qgis/qgis-repo.xml?qgis=' + qgis_version
    ]

    # Create repos dir
    counter = 0
    repos_dir = os.path.join(tempfile.gettempdir(), 'repos')
    if not os.path.exists(repos_dir):
        os.makedirs(repos_dir)
    plugins_dir = os.path.join(tempfile.gettempdir(), 'plugins')
    if not os.path.exists(plugins_dir):
        os.makedirs(plugins_dir)
    for metadata_xml_url in metadata_xml_urls:
        urllib.urlretrieve(metadata_xml_url, os.path.join(repos_dir, str(counter) + ".repo.xml"))
        counter += 1
    for plugin in plugins_list:
        plugin_name1 = plugin
        plugin_name2 = plugin.replace(' ', '_')
        output_url = ''
        version = '0.0.0'
        # list all xml files
        for repo_xml in os.listdir(repos_dir):
            try:
                tree = ET.parse(os.path.join(repos_dir, repo_xml))
                root = tree.getroot()
                for pyqgis_plugin in root.findall('pyqgis_plugin'):
                    if plugin_name1 == pyqgis_plugin.get('name') or plugin_name2 == pyqgis_plugin.get('name'):
                        currentVersion = pyqgis_plugin.get('version').replace('-', '.')
                        if LooseVersion(currentVersion) > LooseVersion(version):
                            version = currentVersion
                            output_url = pyqgis_plugin.find('download_url').text
            except:
                pass

        if output_url:
            out_zip = os.path.join(plugins_dir, plugin_name2 + '.zip')
            urllib.urlretrieve(output_url, out_zip)

            # Extract zip to specific folder
            prev_dir = os.getcwd()
            os.chdir(out_dir)
            run(('cmake', '-E', 'tar', 'xzf', out_zip))
            os.chdir(prev_dir)
