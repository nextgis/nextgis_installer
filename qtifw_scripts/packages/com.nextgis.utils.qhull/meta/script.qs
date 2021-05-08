
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","QHULL utilities"));
    component.setValue("Description",qsTranslate("script","QHULL command line utilities"));
}
