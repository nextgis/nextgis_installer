
var Dir = new function () 
{
    this.toNativeSparator = function (path) 
    {
        if (systemInfo.productType === "windows")
            return path.replace(/\//g, '\\');
        return path;
    }
};


function Component() 
{
    if (installer.isInstaller()) 
    {
        component.loaded.connect(this, Component.prototype.componentLoaded);
    }
}


Component.prototype.componentLoaded = function ()
{  
    component.setValue("Description",qsTranslate("rootscript","All NextGIS programs"));   
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows") 
    {
        component.addOperation("CreateShortcut", 
            "@TargetDir@/maintenancetool.exe", "@StartMenuDir@/NextGIS Updater.lnk", "workingDirectory=@TargetDir@");            
    }
}
