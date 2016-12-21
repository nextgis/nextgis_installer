
var linkCompare = "http://nextgis.com";

function Component() 
{
    if (installer.isInstaller()) 
    {
        component.loaded.connect(this, Component.prototype.componentLoaded);
    }
}


Component.prototype.componentLoaded = function ()
{
    widget = gui.pageWidgetByObjectName("ComponentSelectionPage");
    if (widget != null)
    {
        var versAvail = "1.0";
        var versFresh = "2.2";
        component.setValue("Description",
            qsTranslate("formbuilderscript","Forms creator for NextGIS Mobile")+"<br><br>"
            +qsTranslate("formbuilderscript","Available version: ")+"<b>"+versAvail+"</b><br>"
            +qsTranslate("formbuilderscript","Fresh version: ")+"<b>"+versFresh+"</b><br>"
            +"<a href=\""+linkCompare+"\">"
            +qsTranslate("formbuilderscript","Compare versions")
            +"</a><br>");
        widget.ComponentDescriptionLabel.linkActivated.connect(this, Component.prototype.onClickCompareLink);
    }
}

Component.prototype.onClickCompareLink = function ()
{ 
    QDesktopServices.openUrl(linkCompare);
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows") 
    {
        component.addOperation("CreateShortcut", 
            "@TargetDir@/bin/fb.exe", "@StartMenuDir@/Formbuilder.lnk", "workingDirectory=@TargetDir@/bin");
        component.addOperation("CreateShortcut", 
            "@TargetDir@/bin/fb.exe", "@DesktopDir@/Formbuilder.lnk", "workingDirectory=@TargetDir@/bin");            
    }
}
