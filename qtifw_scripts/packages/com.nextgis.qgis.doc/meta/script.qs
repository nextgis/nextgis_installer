
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","Documentation"));
    component.setValue("Description",qsTranslate("script","QGIS Documentation"));
}
