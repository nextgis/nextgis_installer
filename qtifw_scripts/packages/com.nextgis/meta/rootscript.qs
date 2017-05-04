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
        
        var strTargetDir = installer.value("TargetDir");
        component.addOperation( "AppendFile",
                                "@TargetDir@/run_ng_env.bat",
                                "echo off\n" +
                                "cls\n" +
                                "set PATH=" + strTargetDir + "\\bin;%PATH%\n" +
                                "set PROJ_LIB=" + strTargetDir + "\\share\\proj\n" +
                                "set SSL_CERT_FILE=" + strTargetDir + "\\share\\ssl\\certs\\cert.pem\n" +
                                "set CURL_CA_BUNDLE=" + strTargetDir + "\\share\\ssl\\certs\\cert.pem\n" +
                                "set GDAL_DATA=" + strTargetDir + "\\share\\gdal\n" +
                                "cmd.exe /k\n" +
                                "echo on\n" );

        component.addOperation( "CreateShortcut",
                                "@TargetDir@/run_ng_env.bat",
                                "@StartMenuDir@/NextGIS Command Prompt.lnk" );                                
        
    }
}
