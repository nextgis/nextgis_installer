
function Controller()
{
    installer.aboutCalculateComponentsToInstall.connect(this, Controller.prototype.onCalculateComponents);
    
    var stringName = qsTranslate("initscript","NextGIS programs");
    installer.setValue("Name",stringName);
}

Controller.prototype.ComponentSelectionPageCallback = function()
{
   var widget = gui.currentPageWidget(); 
   if (widget != null) 
    {
        widget.SelectAllComponentsButton.setVisible(false);
        widget.DeselectAllComponentsButton.setVisible(false);
        widget.SelectDefaultComponentsButton.setVisible(false);
        widget.ComponentDescriptionLabel.setWordWrap(true);
    }
}

Controller.prototype.onCalculateComponents = function()
{
    var widget = gui.pageWidgetByObjectName("DynamicPageAuth"); 
    if (widget != null) 
    {
        var login = widget.eLogin.text;
        var pass = widget.ePass.text;
        installer.setValue("UrlQueryString","login="+login+"&password="+pass);
    }
}