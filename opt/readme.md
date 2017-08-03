# Add self update package

**WARNING!** It must not be any changes in /framework or /packages! Only installer
framework changes.

## Requirements

Some software distributed via installer and network repository.

## Steps

1. Build installer (in QtCreator or command line tool)

For example on Mac OS X
```
> python build_installer.py --static-qmake /<path to qt sources>/qtbase/bin/qmake --qt_menu_nib /<path to qt sources>/qtbase/src/plugins/platforms/cocoa/qt_menu.nib --make make --targetdir /<working directory>/qtifw_build/
```

2. Generate repository with create option.

For example on Mac OS X
```
> python create_installer.py -q /<path to qt sources>/qtbase/bin -s /Users/Bishop/work/projects/borsch -t /<working directory>/build-dev2 -i nextgis-setup create
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