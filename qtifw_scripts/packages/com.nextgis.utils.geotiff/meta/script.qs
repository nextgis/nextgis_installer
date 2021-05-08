
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","GeoTIFF utilities"));
    component.setValue("Description",qsTranslate("script","GeoTIFF command line utilities"));
}
