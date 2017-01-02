# Introduction

# Create installer framework

Notes to create installer via Qt InstallerFramework modified for NextGIS
authentication:

## 1. Build OpenSSL from NextGIS Borsch statically

```bash
> git clone https://github.com/nextgis-borsch/lib_openssl.git
> cd lib_openssl
> mkdir build
> cd build
> cmake -WITH_ZLIB -WITH_ZLIB_EXTERNAL ..
> cmake -build . -- -j 4
```

## 2. Build Qt (5.6.0 strictly required on Windows due the UAC bug) statically with OpenSSL linked

### Windows

Example of configure string:

```bash
> configure -prefix %CD%\qtbase -debug-and-release -static -static-runtime -opensource -platform win32-msvc2013 -target xp -accessibility -no-opengl -no-icu -no-sql-sqlite -no-qml-debug -nomake examples -nomake tests -skip qtactiveqt -skip qtlocation -skip qtmultimedia -skip qtserialport -skip qtsensors -skip qtxmlpatterns -skip qtquickcontrols -skip qtquickcontrols2 -skip qt3d -openssl -openssl-linked -I <path to lib_openssl>\include -L <path to lib_openssl>\lib -L "C:\Program Files\Microsoft SDKs\Windows\v7.1\Lib" -l Gdi32 -l User32
```

### Mac OS X

Example of configure string:

```bash
> OPENSSL_LIBS='-L<path to lib_openssl>/build/ssl -L<path to lib_openssl>/lib_openssl/build/crypto -lsslstatic -lcryptostatic' ./configure -prefix $PWD/qtbase -release -static -opensource -confirm-license -accessibility -no-opengl -no-icu -no-sql-sqlite -no-qml-debug -nomake examples -nomake tests -skip qtactiveqt -skip qtlocation -skip qtmultimedia -skip qtserialport -skip qtsensors -skip qtxmlpatterns -skip qtquickcontrols -skip qtquickcontrols2 -skip qt3d -openssl-linked -I <path to lib_openssl>/lib_openssl/build/include -L<path to lib_openssl>/lib_openssl/build/ssl -L<path to lib_openssl>/lib_openssl/build/crypto
```

## 3. Build InstallerFramework

Note: To build installer framework via build_installer script python required.

```bash
> cd <path to this repo>/qtifw/tools
> python build_installer.py --static-qmake <path to Qt bin files>/qmake --make make --targetdir <path to build directory> --qt_menu_nib <path to static QT>/qtbase/src/plugins/platforms/cocoa
```

## 4. Create NextGIS installer

### 4.1 Generating installer:

Note: To create installer via create_installer script python required.

```bash
> cd <path to this repo>/opt
> python create_installer.py create -t <output path> -q <path to Qt bin files> -s <path to packages sources root (borsch root)> -r http://<path to network folder> -n
```

### 4.2 Updating existing packages:

```bash
> cd <path to this repo>/opt
> python create_installer.py update -t <output path> -q <path to Qt bin files> -s <path to packages sources root (borsch root)> -r http://<path to network folder> -n
```

# Packages structure

All package metadata stored in qtifw_scripts/packages directory. All packages must
have own directory started with 'com.nextgis'. In each directory must be two
folders:
* data
* meta

In each folder must be 'package.xml' file. Also scripts (\*.qs), translations
(\*.ts) files may be present.

In data folder the package.xml should looks like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package root="repository folder name">
    <Version>1.0</Version> <!-- **optional** Package version. For virtual package usually 1.0 and **required**. For real package in form of major.minor.patch-build (iterate automatically) -->
    <UpdateText></UpdateText> <!-- **optional** Some text for next version or build -->
    <win src="" dst=""/> <!-- **optional** src - Path from borsch root directory for install files. dst - path in package folder to copy install files -->
    <mac src="" dst=""/> <!-- **optional** -->
</Package>
```

The description of package.xml in meta folder see in [this link](http://doc.qt.io/qtinstallerframework/ifw-component-description.html#package-directory-structure)
The \<Version\> tag will be overwritten by value from version.str of build folder in sources or xml tag in data folder (for groups).
The \<ReleaseDate\> will be set on current date. Both tags can be skipped in package.xml
in meta folder.

According to this structure create_installer script will form needed folders and
files in target directory and generate installer (nextgis-setup).

# Links

* [Tutorial: Creating an Installer](http://doc.qt.io/qtinstallerframework/ifw-tutorial.html)
* [Package Directory](http://doc.qt.io/qtinstallerframework/ifw-component-description.html#package-directory-structure)
* [Configuration File](http://doc.qt.io/qtinstallerframework/ifw-globalconfig.html)
* [Component Scripting](http://doc.qt.io/qtinstallerframework/scripting.html)
* [Qt for macOS - Deployment](http://doc.qt.io/qt-5/osx-deployment.html)
