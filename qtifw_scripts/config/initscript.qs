
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

function Component()
{
	var page = gui.pageByObjectName("FinishedPage");
	page.entered.connect(Component.prototype.finishPageEntered);
}

Component.prototype.finishPageEntered = function()
{
	gui.setWizardPageButtonText(QInstaller.InstallationFinished, buttons.CommitButton, "Debug");
    buttons.CommitButton.hide();
}

Controller.prototype.FinishedPageCallback = function()
{
    gui.pageById(QInstaller.Finished).showRestartRequired = false;
}