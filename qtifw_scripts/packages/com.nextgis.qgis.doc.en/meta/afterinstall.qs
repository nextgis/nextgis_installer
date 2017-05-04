
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","QGIS documentation"));
    component.setValue("Description",qsTranslate("script","QGIS documentation"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        component.addOperation("CreateShortcut",
            "@TargetDir@/share/doc/ngqgis/NextGIS_QGIS_en.pdf", "@StartMenuDir@/QGIS user guide.lnk", "workingDirectory=@TargetDir@/share/doc/ngqgis");   
    }
}
