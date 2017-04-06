
function Controller()
{
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
