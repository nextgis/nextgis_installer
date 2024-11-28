
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
    installer.updateFinished.connect(this, onUpdateFinished);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","QGIS python"));
    component.setValue("Description",qsTranslate("script","QGIS python"));
}

onUpdateFinished = function()
{
    if (!installer.isUpdater() || installer.status != QInstaller.Success) {
        return;
    }

    if ( installer.value("os") == "win")
    {
        var qtilesDir = installer.value("TargetDir") + "/share/ngqgis/python/plugins/qtiles";
        installer.execute("cmd", ["/c", "if exist \"" + qtilesDir + "\" rd /s /q \"" + qtilesDir + "\""]);
    }
    else if ( installer.value("os") == "mac")
    {
        var qtilesDir = installer.value("TargetDir") + "/Applications/qgis-ng.app/Contents/Resources/python/plugins/qtiles";
        // TODO
    }
}
