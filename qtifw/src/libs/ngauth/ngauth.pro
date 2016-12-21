QT = network

TEMPLATE = lib
include(../../../installerfw.pri)

TARGET = ngauth
INCLUDEPATH += . ..

CONFIG += staticlib

DEFINES += BUILD_LIB_INSTALLER

DESTDIR = $$IFW_LIB_PATH
DLLDESTDIR = $$IFW_APP_PATH

HEADERS += ngaccess.h \
           simplecrypt.h

SOURCES += ngaccess.cpp \
           simplecrypt.cpp
