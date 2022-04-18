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
    }
    else if (installer.value("os") == "mac")
    {
        component.addOperation( "Mkdir",
                                "@HomeDir@/Library/Python/2.7/lib/python/site-packages" );
        component.addOperation( "Delete",
                                "@HomeDir@/Library/Python/2.7/lib/python/site-packages/NextGIS.pth" );
        component.addOperation( "AppendFile",
                                "@HomeDir@/Library/Python/2.7/lib/python/site-packages/NextGIS.pth",
                                "@TargetDir@/Library/Python/2.7/site-packages\n@TargetDir@/Library/Python/2.7/site-packages/osgeo" );
    }
}
