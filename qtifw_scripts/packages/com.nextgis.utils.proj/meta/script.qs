
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","Proj utilities"));
    component.setValue("Description",qsTranslate("script","Proj command line utilities"));
}
