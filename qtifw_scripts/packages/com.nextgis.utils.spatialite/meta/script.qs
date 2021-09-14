
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","Spatialite utilities"));
    component.setValue("Description",qsTranslate("script","Spatialite command line utilities"));
}
