
function Component()
{

}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        component.addOperation("CreateShortcut",
            "@TargetDir@/share/doc/ngqgis/NextGIS_QGIS_ru.pdf", "@StartMenuDir@/NextGIS QGIS руководство.lnk", "workingDirectory=@TargetDir@/share/doc/ngqgis");
    }
}
