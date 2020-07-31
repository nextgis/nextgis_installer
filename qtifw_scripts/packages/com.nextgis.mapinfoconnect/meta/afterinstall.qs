function Component()
{
    component.loaded.connect(this, Component.prototype.componentLoaded);
}

Component.prototype.componentLoaded = function ()
{
    component.setValue("DisplayName",qsTranslate("script","NextGIS Connect for MapInfo"));
    component.setValue("Description",qsTranslate("script","MapInfo Pro extension which allows to connect to your Web GIS at nextgis.com and manage its resources"));
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (systemInfo.productType === "windows")
    {
        var plugin_path = "@TargetDir@\\share\\NextGIS\\MapInfo\\NextGISConnect";
        
        // Define architecture type of installer (not the system).
        var repo_url = component.repositoryUrl.toString();
        var is_installer_x64 = false;
        if (repo_url.indexOf("64") != -1)
            is_installer_x64 = true;
        
        var versions = ["900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700"];
        for (var i = 0; i < versions.length; i++)
        {
            var reg_path = "HKEY_CURRENT_USER\\Software\\MapInfo\\MapInfo\\Professional\\" + versions[i];
            // TODO: add registry keys only for existing versions of MapInfo. 
            // We need a way how to find an existing registry key. How to check the result of REG QUERY here?
            /*
                REG QUERY HKEY_CURRENT_USER\Software\MapInfo\MapInfo\Professional\1700\Tools64\99999
                IF %ERRORLEVEL% EQU 0 (
                   echo Found key
                ) ELSE (
                    echo Did not found key
                )
            */
            
            if (is_installer_x64)
                reg_path += "\\Tools64";
            else 
                reg_path += "\\Tools";

            reg_path += "\\99999"; 
            // TODO: add checks whether "99999" already exists in registry and pick another name if so.

            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Autoload", "/t", "REG_DWORD", "/d", "1");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Description", "/t", "REG_SZ", "/d", "NextGIS Connect for MapInfo");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "ImageUri", "/t", "REG_SZ", "/d", plugin_path + "\\nextgis.png");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Location", "/t", "REG_SZ", "/d", plugin_path + "\\NextGISConnect.mbx");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Owner", "/t", "REG_SZ", "/d", "MI_TOOLS");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Title", "/t", "REG_SZ", "/d", "NextGIS Connect");
            
            // The following command is for deinstallation step only:
            component.addElevatedOperation("Execute", "ECHO", "Registry modified", "UNDOEXECUTE", "REG", "DELETE", reg_path, "/f");
        }
    }
}
