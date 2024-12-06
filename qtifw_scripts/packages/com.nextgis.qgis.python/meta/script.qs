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

    if (systemInfo.productType === "windows")
    {
        var qtilesDir = installer.value("TargetDir") + "/share/ngqgis/python/plugins/qtiles";
        if (installer.fileExists(qtilesDir))
        {
            component.addOperation("Execute", "cmd", "/c", "rd", "/s", "/q", qtilesDir);
        }
    }
}
