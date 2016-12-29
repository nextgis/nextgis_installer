/*******************************************************************************
**
** Project: NextGIS online/offline installer
** Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
** Copyright (c) 2016 NextGIS <info@nextgis.com>
** License: GPL v.2
**
*******************************************************************************/

var Dir = new function ()
{
    this.toNativeSparator = function (path)
    {
        if (systemInfo.productType === "windows")
            return path.replace(/\//g, '\\');
        return path;
    }
};


function Component()
{
    if (installer.isInstaller())
    {
        component.loaded.connect(this, Component.prototype.componentLoaded);
    }
}


Component.prototype.componentLoaded = function ()
{
    component.setValue("Description",qsTranslate("rootscript","All NextGIS programs"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    // Create uninstall link only for windows
    if (installer.value("os") == "win")
    {
        // shortcut to uninstaller
        component.addOperation( "CreateShortcut",
                                "@TargetDir@/nextgisupdater.exe",
                                "@StartMenuDir@/Uninstall NextGIS.lnk",
                                " --uninstall");
    }
    // only for windows online installer
    if ( installer.value("os") == "win" && !installer.isOfflineOnly() )
    {
        // create shortcut
        component.addOperation( "CreateShortcut",
                                "@TargetDir@/nextgisupdater.exe",
                                "@StartMenuDir@/NextGIS Maintenance Tool.lnk",
                                "workingDirectory=@TargetDir@" );
    }
}
