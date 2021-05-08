
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","GDAL utilities"));
    component.setValue("Description",qsTranslate("script","GDAL command line utilities"));
}