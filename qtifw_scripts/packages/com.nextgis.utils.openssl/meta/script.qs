
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","OpenSSL utilities"));
    component.setValue("Description",qsTranslate("script","OpenSSL command line utilities"));
}
