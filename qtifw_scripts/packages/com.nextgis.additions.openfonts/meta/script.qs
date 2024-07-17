
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","OpenSans fonts"));
    component.setValue("Description",qsTranslate("script","A set of free fonts: OpenSans, DejaVu and STIX fonts family"));
}
