
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","OpenCV utilities"));
    component.setValue("Description",qsTranslate("script","OpenCV command line utilities"));
}
