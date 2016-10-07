Qt Installer Framework test

Example commands for Windows:

0. Before generating installer check the main config.xml file for the repository url.
For online installer should be: http://176.9.38.120/installer/repository-free
For offline installer something like: file:///D:/github/nextgis_installer/qtifw_scripts/repository-free

1. Generating installer:
> cd /d D:\nextgis\installer\test
> C:\Qt\QtIFW2.0.3\bin\repogen.exe --remove -v -p packages repository-free
> C:\Qt\QtIFW2.0.3\bin\binarycreator.exe -v --online-only -c config\config.xml -p packages nextgis-installer

2. Translations:
> cd /d D:\nextgis\installer\test\packages\com.nextgis\meta
> C:\Qt\Qt5.7.0\5.7\msvc2013\bin\lupdate.exe page_auth.ui rootscript.qs -ts ru.ts
> C:\Qt\Qt5.7.0\5.7\msvc2013\bin\lrelease.exe ru.ts
> cd /d D:\nextgis\installer\test\packages\com.nextgis.formbuilder\meta
> C:\Qt\Qt5.7.0\5.7\msvc2013\bin\lupdate.exe formbuilderscript.qs -ts ru.ts
> C:\Qt\Qt5.7.0\5.7\msvc2013\bin\lrelease.exe ru.ts

3. Generating updates:
> cd /d D:\nextgis\installer\test
> C:\Qt\QtIFW2.0.3\bin\repogen.exe --update-new-components -p packages repository-free