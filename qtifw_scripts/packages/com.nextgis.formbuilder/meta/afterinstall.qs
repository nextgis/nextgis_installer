
function Component() 
{

}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows") 
    {
        component.addOperation("CreateShortcut", 
            "@TargetDir@/bin/fb.exe", "@DesktopDir@/NextGIS Formbuilder.lnk", "workingDirectory=@TargetDir@/bin"); 
        component.addOperation("CreateShortcut", 
            "@TargetDir@/bin/fb.exe", "@StartMenuDir@/NextGIS Formbuilder.lnk", "workingDirectory=@TargetDir@/bin");            
    }
}
