TEMPLATE = subdirs
SUBDIRS += 7zip ngauth installer
installer.depends = 7zip ngauth
