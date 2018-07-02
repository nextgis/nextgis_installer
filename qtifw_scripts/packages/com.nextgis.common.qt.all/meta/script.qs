/*******************************************************************************
**
** Project: NextGIS online/offline installer
** Author: Mikhail Gusev <gusevmihs@gmail.com>
** Copyright (c) 2017 NextGIS <info@nextgis.com>
** License: GPL v.2
**
*******************************************************************************/

function Component()
{
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") == "win")
    {
		var strTargetDir = installer.value("TargetDir");
		var strTargetDirRepl = strTargetDir.replace(/\\/g,'/');
        // make dir
        component.addOperation( "Mkdir", "@TargetDir@/bin" );
        component.addOperation( "AppendFile",
                                "@TargetDir@/bin/qt.conf",
								"[Paths]\n" +
                                "Prefix = " + strTargetDirRepl + "\n" +
								"4/Translations = share/qt4/translations\n" +
								"4/Plugins = lib/qt4/plugins\n" +
								"Translations = share/qt5/translations\n" +
								"Plugins = lib/qt5/plugins" );
    }

    if (installer.value("os") == "mac")
    {

    }
}
