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

    if (installer.value("os") == "mac")
    {
        component.addOperation( "AppendFile",
                                "@HomeDir@/.bash_profile",
                                "\nexport PATH=$PATH:@TargetDir@/usr/bin" );
    }
}
