
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","EXPAT utilities"));
    component.setValue("Description",qsTranslate("script","EXPAT command line utilities"));
}