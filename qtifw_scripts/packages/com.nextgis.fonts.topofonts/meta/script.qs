
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","Topographic fonts"));
    component.setValue("Description",qsTranslate("script","A set of topographic fonts"));
}
