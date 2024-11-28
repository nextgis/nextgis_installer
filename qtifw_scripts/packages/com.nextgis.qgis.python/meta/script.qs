
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","QGIS python"));
    component.setValue("Description",qsTranslate("script","QGIS python"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (!installer.isUpdater())
    {
        return;
    }
    if ( installer.value("os") == "win")
    {
        var qtilesDir = installer.value("TargetDir") + "/share/ngqgis/python/plugins/qtiles";
        if (installer.fileExists(qtilesDir))
        {
            installer.execute("cmd", ["/c", "rd /s /q \"" + qtilesDir + "\""]);
        }
    }
    else if ( installer.value("os") == "mac")
    {
        var qtilesDir = installer.value("TargetDir") + "/Applications/qgis-ng.app/Contents/Resources/python/plugins/qtiles";
        // TODO
    }
}