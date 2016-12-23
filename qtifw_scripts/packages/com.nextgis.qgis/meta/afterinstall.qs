
function Component() 
{

}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows") 
    {
        component.addOperation("CreateShortcut", 
            "@TargetDir@/bin/ngq.bat", "@DesktopDir@/NextGIS QGIS.lnk", "workingDirectory=@TargetDir@", "iconPath=@TargetDir@/bin/ngqgis.exe");
        component.addOperation("CreateShortcut", 
            "@TargetDir@/bin/ngq.bat", "@StartMenuDir@/NextGIS QGIS.lnk", "workingDirectory=@TargetDir@", "iconPath=@TargetDir@/bin/ngqgis.exe");            
    }
}
