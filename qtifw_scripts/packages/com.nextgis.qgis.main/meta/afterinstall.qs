
function Component() 
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","QGIS main"));
    component.setValue("Description",qsTranslate("script","QGIS Application main files"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        component.addOperation("CreateShortcut",
            "@TargetDir@/bin/ngqgis.exe", "@DesktopDir@/NextGIS QGIS.lnk", "workingDirectory=@TargetDir@", "iconPath=@TargetDir@/bin/ngqgis.exe");
        component.addOperation("CreateShortcut",
            "@TargetDir@/bin/ngqgis.exe", "@StartMenuDir@/NextGIS QGIS.lnk", "workingDirectory=@TargetDir@", "iconPath=@TargetDir@/bin/ngqgis.exe");
    }

    if (installer.value("os") == "mac")
    {
        component.addOperation("LineReplace",
            "@TargetDir@/Applications/qgis-ng.app/Contents/Resources/qt.conf",
            "Prefix = ", "Prefix = @TargetDir@");
        component.addOperation("CreateLink", "@HomeDir@/Applications/NextGIS QGIS.app", "@TargetDir@/Applications/qgis-ng.app" );
    }
}
