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
                                "PROJ_LIB",
                                "@TargetDir@/share/proj" );
    }
    else if (installer.value("os") == "mac")
    {
        component.addOperation( "AppendFile",
                                "@HomeDir@/.bash_profile",
                                "\nexport PROJ_LIB=@TargetDir@/Library/Frameworks/proj.framework/Resources/proj" );
    }
}
