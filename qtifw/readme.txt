Notes to create installer via Qt InstallerFramework modified for NextGIS authentication:

1) Build Qt (5.6.0 strictly required) statically with OpenSSL linked.
Example of configure string:

configure -prefix %CD%\qtbase -debug-and-release -static -static-runtime -opensource -platform win32-msvc2013 -target xp -accessibility -no-opengl -no-icu -no-sql-sqlite -no-qml-debug -nomake examples -nomake tests -skip qtactiveqt -skip qtlocation -skip qtmultimedia -skip qtserialport -skip qtsensors -skip qtxmlpatterns -skip qtquickcontrols -skip qtquickcontrols2 -skip qt3d -openssl -openssl-linked -I D:\libs\openssl-1.0.1-x86-build\include -L D:\libs\openssl-1.0.1-x86-build\lib -L "C:\Program Files\Microsoft SDKs\Windows\v7.1\Lib" -l Gdi32 -l User32

2) Clone modified InstallerFramework https://github.com/MikhanGusev/installer-framework;

3) Build InstallerFramework;

4) Create NextGIS installer.
Example commands for Windows:

* Before generating installer check the main config.xml file for the repository url.
For online installer should be: http://176.9.38.120/installer/repository-free
For offline installer something like: file:///D:/github/repository-free

* Generating installer:
> cd <path-to-this-repo>
> <path-to-framework>\repogen.exe --remove -v -p packages repository-free
> <path-to-framework>\binarycreator.exe -v --online-only -c config\config.xml -p packages nextgis-setup

