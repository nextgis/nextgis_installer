
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","CURL utilities"));
    component.setValue("Description",qsTranslate("script","CURL command line utilities"));
}