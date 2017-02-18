
function Component()
{

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
