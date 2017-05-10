
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","QCA utilities"));
    component.setValue("Description",qsTranslate("script","QCA command line utilities"));
}
