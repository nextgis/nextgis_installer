# Add self update package

**WARNING!** It must not be any changes in /framework or /packages! Only installer
framework changes.

## Requirements

Some software distributed via installer and network repository.

## Steps

### New

1. Build new installer via buildbot
2. Start virtual PS
3. Clone installer repository

```
> git clone --depth 1 https://github.com/nextgis/nextgis_installer
> cd nextgis_installer
```

4. Execute script

```
> python opt/create_updater.py -i nextgis-setup-<mac | win32>-dev -v '3.0.1' --ftp_user <name:password> --ftp ftp://192.168.255.51/software/installer --ftpout_user <name:password> --ftpout ftp://192.168.245.1:8121/software/installer
```

5. Update installer via buildbot. In force field add ``com.nextgis.nextgis_installer`` package name.

**NOTE:** Working directory is important!

### Old

1. Build new installer (via buildbot, in QtCreator or command line tool)

For example on Mac OS X
```
> python build_installer.py --static-qmake /<path to qt sources>/qtbase/bin/qmake --qt_menu_nib /<path to qt sources>/qtbase/src/plugins/platforms/cocoa/qt_menu.nib --make make --targetdir /<working directory>/qtifw_build/
```

2. Generate repository with create option.

For example on Mac OS X
```
> python create_installer.py -q /<path to qt sources>/qtbase/bin -s /<working directory>/projects/borsch -t /<working directory>/build-dev2 -i nextgis-setup create
```

3. Install created installer in some temporary folder to get nextgisupdater
   application.

4. Create if not exists package in /qtifw_scripts, with name com.nextgis.nextgis_updater and
   add <Essential> and <Virtual> tags. If exists - update version in build/version.str file

5. Copy nextgisupdater in package data directory preserved directory structure.
   For Windows it will be 3 files dat, exe and ini named nextgisupdater. For MacOS
   X it will be - dat, app and ini.

6. Update original repository.

For example on Windows for standalone installer
```
    > python create_installer.py -q <path to qt sources>\qtbase\bin -t C:\nextgis\nextgis_installer_OUTPUT -s C:\nextgis\nextgis_installer_PACKAGE_SOURCES -r file:///C:\nextgis\nextgis_installer_OUTPUT\repository-win -n update --force com.nextgis.nextgis_updater
```

7. Upload new repository to site replacing previous one.

8. Delete temporary directory for installed installer from step 3.

9. Don't change updater package (not needed to remove <Essential> tag).

## Checks

1. Only one update for installer received.

2. Force to update package com.nextgis.nextgis_updater      

# Add new package

1. Add package description to qtifw_scripts
2. Add package repository name to opt/create_installer.py
3. Add package repository name and build arguments to buildbot/makeborsch.py
4. Force update in Buildbot. Add package name in update page.

**NOTE**: git push start update installer repository automatically if 1-4 steps
completed.

Buildbot has 3 builders:

* create_installer_mac
* create_installer_win32
* create_installer_win64

Each builder has ``Create installer`` and ``Update installer`` buttons to force
build or update installer. In force dialog you can choose installer and repository
suffix (default is ``-dev``, empty string also permitted). You can add specific
packages to update (space is delimiter) or ``all`` to force all packages.

# TODO

Add create standalone installer option to ``Create installer`` force button dialog.
