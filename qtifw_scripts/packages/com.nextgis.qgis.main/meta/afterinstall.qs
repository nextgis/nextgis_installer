
function Component()
{

}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        component.addOperation("CreateShortcut",
            "@TargetDir@/bin/ngq.bat", "@DesktopDir@/NextGIS QGIS.lnk", "workingDirectory=@TargetDir@", "iconPath=@TargetDir@/bin/ngqgis.exe");
        component.addOperation("CreateShortcut",
            "@TargetDir@/bin/ngq.bat", "@StartMenuDir@/NextGIS QGIS.lnk", "workingDirectory=@TargetDir@", "iconPath=@TargetDir@/bin/ngqgis.exe");
    }

    if (installer.value("os") == "mac")
    {
        component.addOperation("LineReplace",
            "@TargetDir@/Applications/ngqgis.app/Contents/Resources/qt.conf",
            "Prefix = ", "Prefix = @TargetDir@");
        component.addOperation("CreateLink", "@HomeDir@/Applications/NextGIS QGIS.app", "@TargetDir@/Applications/ngqgis.app" );
    }
}
