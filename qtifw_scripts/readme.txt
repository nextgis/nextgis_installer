Qt Installer Framework test

Commands for Windows ():

1. Translations:
> cd /d D:\nextgis\installer\test\packages\com.nextgis\meta
> C:\Qt\Qt5.7.0\5.7\msvc2013\bin\lupdate.exe page_auth.ui rootscript.qs -ts ru.ts
> C:\Qt\Qt5.7.0\5.7\msvc2013\bin\lrelease.exe ru.ts
> cd /d D:\nextgis\installer\test\packages\com.nextgis.formbuilder\meta
> C:\Qt\Qt5.7.0\5.7\msvc2013\bin\lupdate.exe formbuilderscript.qs -ts ru.ts
> C:\Qt\Qt5.7.0\5.7\msvc2013\bin\lrelease.exe ru.ts

2. Generating installer:
> cd /d D:\nextgis\installer\test
> C:\Qt\QtIFW2.0.3\bin\repogen.exe --remove -v -p packages repository-free
> C:\Qt\QtIFW2.0.3\bin\binarycreator.exe -v --online-only -c config\config.xml -p packages nextgis-installer

3. Generating updates:
> cd /d D:\nextgis\installer\test
> C:\Qt\QtIFW2.0.3\bin\repogen.exe --update-new-components -p packages repository-free