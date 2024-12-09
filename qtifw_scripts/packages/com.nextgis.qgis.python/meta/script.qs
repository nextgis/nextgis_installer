var Dir = new function () {
    this.toNativeSparator = function (path) {
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
    component.setValue("DisplayName",qsTranslate("script","QGIS python"));
    component.setValue("Description",qsTranslate("script","QGIS python"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        var targetDir = Dir.toNativeSparator(installer.value("TargetDir"));
        var qtilesDir = targetDir + "\\share\\ngqgis\\python\\plugins\\qtiles";

        if (installer.fileExists(qtilesDir))
        {
            component.addOperation("Execute", "cmd", "/c", "rd", "/s", "/q", qtilesDir);
        }
    }
}
