@echo off
set PATH=TargetDir;TargetDir\bin;%SystemRoot%\system32
set PROJ_LIB=TargetDir\share\proj
set SSL_CERT_FILE=TargetDir\share\ssl\certs\cert.pem
set CURL_CA_BUNDLE=TargetDir\share\ssl\certs\cert.pem
set GDAL_DATA=TargetDir\share\gdal
@echo on
@echo. & @echo ************************************************************ & @echo ** Welcome to NextGIS Command Prompt & @echo ** Copyright (C) 2011-2021, NextGIS & @echo ************************************************************ & @echo. & cmd.exe /k
