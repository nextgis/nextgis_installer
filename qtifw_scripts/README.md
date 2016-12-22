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

## 2. Build Qt (5.6.0 strictly required on Windows due the UAC bug) statically with OpenSSL linked.

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

## 3. Go to installer framework folder

```bash
> cd ../qtifw
```

## 4. Build InstallerFramework

Note: To build installer framework via build_installer script python required.

```bash
> cd tools
> ./build_installer.py --static-qmake <path to static QT>/qtbase/bin/qmake --make make --targetdir <path to build directory>/ --qt_menu_nib <path to static QT>/qtbase/src/plugins/platforms/cocoa
```

## 5. Create NextGIS installer.

### 5.1 Before generating installer check the main config.xml file for the repository url.

* For online installer should be: http://176.9.38.120/installer/repository-free
* For offline installer something like: file:///D:/github/repository-free

### 5.2 Generating installer:

### Windows

```bash
> cd <path to this repo>
> <path to framework>\repogen.exe --remove -v -p packages repository-free
> <path to framework>\binarycreator.exe -v --online-only -c config\config.xml -p packages nextgis-setup
```

### Mac OS X

```bash
> ./repogen --remove -v -p <path to repo structure>/mac/packages <output path>/repository-mac
> ./binarycreator -v --offline-only -c <path to repo structure>/mac/config/config.xml -p <path to repo structure>/mac/packages <output path>/nextgis-setup
```

### 5.3 Updating existing packages:

### Windows
```bash
> cd <path to this repo>
> <path to framework>\repogen.exe --update-new-components -p packages repository-free
```
