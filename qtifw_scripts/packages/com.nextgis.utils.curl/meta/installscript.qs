/*******************************************************************************
**
** Project: NextGIS online/offline installer
** Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
** Copyright (c) 2017 NextGIS <info@nextgis.com>
** License: GPL v.2
**
*******************************************************************************/

function Component()
{

}

function CreateSymLink(name)
{
    component.addOperation("Execute", "{0}", "ln", "-s",
        "@TargetDir@/Applications/curl.app/Contents/MacOS/" + name,
        "@TargetDir@/usr/bin/" + name);
    component.registerPathForUninstallation("@TargetDir@/usr/bin/" + name);
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") == "mac")
    {
        var utilities = [
            "curl"
        ];

        for ( i = 0; i < utilities.length; i++ ) {
            CreateSymLink(utilities[i]);
        }
    }
}
