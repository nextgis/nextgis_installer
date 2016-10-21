
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