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
        var targetDir = installer.value("TargetDir")
        var qtilesDir = (targetDir + "/share/ngqgis/python/plugins/qtiles").replace(/\//g, "\\");
        component.addOperation("Execute", "cmd", "/c", "if exist", qtilesDir, "rd", "/s", "/q", qtilesDir);
    }
}
