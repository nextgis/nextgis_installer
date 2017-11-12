
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","GIF utilities"));
    component.setValue("Description",qsTranslate("script","GIF command line utilities"));
}
