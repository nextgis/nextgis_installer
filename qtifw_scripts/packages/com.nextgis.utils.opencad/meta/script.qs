
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","OpenCAD utilities"));
    component.setValue("Description",qsTranslate("script","OpenCAD command line utilities"));
}
