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
    component.setValue("DisplayName",qsTranslate("rootscript","All"));
    component.setValue("Description",qsTranslate("rootscript","All NextGIS programs"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    // only for windows online installer
    if ( installer.value("os") == "win")
    {
        // create shortcut
        component.addOperation( "CreateShortcut",
                                "@TargetDir@/nextgisupdater.exe",
                                "@StartMenuDir@/NextGIS Maintenance Tool.lnk",
                                " --updater");
    }
}
