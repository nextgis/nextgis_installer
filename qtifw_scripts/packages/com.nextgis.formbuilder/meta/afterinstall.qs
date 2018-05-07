
function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("afterinstall","Formbuilder"));
    component.setValue("Description",qsTranslate("afterinstall","Forms builder for NextGIS Mobile"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        component.addOperation("CreateShortcut",
            "@TargetDir@/bin/fb.exe", "@DesktopDir@/NextGIS Formbuilder.lnk", "workingDirectory=@TargetDir@/bin");
        component.addOperation("CreateShortcut",
            "@TargetDir@/bin/fb.exe", "@StartMenuDir@/NextGIS Formbuilder.lnk", "workingDirectory=@TargetDir@/bin");
    }

    if (installer.value("os") == "mac")
    {
        component.addOperation("LineReplace",
            "@TargetDir@/Applications/fb.app/Contents/Resources/qt.conf",
            "Prefix = ", "Prefix = @TargetDir@");
    }
}
