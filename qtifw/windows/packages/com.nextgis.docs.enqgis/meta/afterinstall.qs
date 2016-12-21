
function Component() 
{

}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows") 
    {
        component.addOperation("CreateShortcut", 
            "@TargetDir@/share/doc/ngqgis/UserGuide_en.pdf", "@StartMenuDir@/QGIS user guide.lnk", "workingDirectory=@TargetDir@/share/doc/ngqgis");   
    }
}
