
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","NextGIS utilities"));
    component.setValue("Description",qsTranslate("script","Various NextGIS console utilities"));
}