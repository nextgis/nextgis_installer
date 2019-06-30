
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","Manuscript"));
    component.setValue("Description",qsTranslate("script","reStructured text and Sphinx documentation editor"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        component.addOperation("CreateShortcut",
            "@TargetDir@/bin/manuscript.exe", "@DesktopDir@/NextGIS Manuscript.lnk", "workingDirectory=@TargetDir@/bin", "iconPath=@TargetDir@/bin/manuscript.exe");
        component.addOperation("CreateShortcut",
            "@TargetDir@/bin/manuscript.exe", "@StartMenuDir@/NextGIS Manuscript.lnk", "workingDirectory=@TargetDir@/bin", "iconPath=@TargetDir@/bin/manuscript.exe");
    }

    if (installer.value("os") == "mac")
    {
        component.addOperation("LineReplace",
            "@TargetDir@/Applications/fb.app/Contents/Resources/qt.conf",
            "Prefix = ", "Prefix = @TargetDir@");
    }
}
