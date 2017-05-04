
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","QGIS plugins"));
    component.setValue("Description",qsTranslate("script","QGIS plugins"));
}