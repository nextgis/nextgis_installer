
var linkGetID = "http://nextgis.com";
var linkForgotPass = "http://nextgis.ru";

var Dir = new function () 
{
    this.toNativeSparator = function (path) 
    {
        if (systemInfo.productType === "windows")
            return path.replace(/\//g, '\\');
        return path;
    }
};


function Component() 
{
    if (installer.isInstaller()) 
    {
        component.loaded.connect(this, Component.prototype.componentLoaded);
    }
}


Component.prototype.componentLoaded = function ()
{  
    component.setValue("Description",qsTranslate("rootscript","All NextGIS programs"));
    
    if (!installer.addWizardPage(component, "PageAuth", QInstaller.ComponentSelection)) 
    {
        console.log("Could not add PageAuth");
    } 
    else
    {
        var widget = gui.pageWidgetByObjectName("DynamicPageAuth");
        if (widget != null) 
        {
            widget.labGetId.text = qsTranslate("rootscript","%1Get NextGIS ID now!%2")
                .arg("<a href=\""+linkGetID+"\">").arg("</a>");
            widget.labGetId.linkActivated.connect(this, Component.prototype.onClickGetNextgisLink);
            widget.labForget.text = qsTranslate("rootscript","%1Forgot password?%2")
                .arg("<a href=\""+linkForgotPass+"\">").arg("</a>");
            widget.labForget.linkActivated.connect(this, Component.prototype.onClickPasswordLink); 
        }
    }   
}


Component.prototype.onClickGetNextgisLink = function ()
{ 
    QDesktopServices.openUrl(linkGetID);
}
Component.prototype.onClickPasswordLink = function ()
{ 
    QDesktopServices.openUrl(linkForgotPass);
}
