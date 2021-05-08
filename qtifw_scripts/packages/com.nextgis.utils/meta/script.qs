
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","Utilities"));
    component.setValue("Description",qsTranslate("script","Utility applications"));
}