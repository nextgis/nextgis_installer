/*******************************************************************************
**
** Project: NextGIS online/offline installer
** Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
** Copyright (c) 2016 NextGIS <info@nextgis.com>
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
        component.addOperation( "EnvironmentVariable",
                                "GDAL_DATA",
                                "@TargetDir@/usr/share/gdal/data" );
    }
    else if (installer.value("os") == "mac")
    {
        component.addOperation( "AppendFile",
                                "@HomeDir@/.bash_profile",
                                "\nexport GDAL_DATA=@TargetDir@/Library/Frameworks/gdal.framework/Resources/data" );
    }
}
