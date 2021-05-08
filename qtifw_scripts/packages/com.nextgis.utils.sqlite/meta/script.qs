
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","SQLite3 utilities"));
    component.setValue("Description",qsTranslate("script","SQLite3 command line utilities"));
}
