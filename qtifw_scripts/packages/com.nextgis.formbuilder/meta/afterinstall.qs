
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("Description",qsTranslate("afterinstall","Forms builder for NextGIS Mobile"));
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
