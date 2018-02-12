/*******************************************************************************
**
** Project: NextGIS online/offline installer
** Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
** Copyright (c) 2016-2018 NextGIS <info@nextgis.com>
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
    component.loaded.connect(this, Component.prototype.componentLoaded);
}


Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("rootscript","All"));
    component.setValue("Description",qsTranslate("rootscript","All NextGIS programs"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if ( installer.value("os") == "win")
    {
        component.addOperation( "CreateShortcut",
                                "@TargetDir@/nextgisupdater.exe",
                                "@StartMenuDir@/NextGIS Maintenance Tool.lnk",
                                " --updater");

        component.addOperation( "Replace",
                                "@TargetDir@/run_ng_env.bat",
                                "TargetDir",
                                "@TargetDir@" );

        component.addOperation( "CreateShortcut",
                                "@TargetDir@/run_ng_env.bat",
                                "@StartMenuDir@/NextGIS Command Prompt.lnk" );

        component.addOperation( "NgUserPathWinEnvironmentVariable",
                                "@TargetDir@" );
    }

    if ( installer.value("os") == "mac")
    {
        component.addOperation( "NgCopyOnly",
                            "@HomeDir@/.bash_profile",
                            "@HomeDir@/.bash_profile.ngbackup");
    }
}
