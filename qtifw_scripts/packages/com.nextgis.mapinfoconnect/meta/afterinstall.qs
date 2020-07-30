function Component()
{
    
}

Component.prototype.createOperations = function()
{
    component.createOperations();
    
    if (systemInfo.productType === "windows")
    {
        var versions = ["900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700"];
        for (var i = 0; i < versions.length; i++)
        {
            var reg_ver_path = "HKEY_CURRENT_USER\\Software\\MapInfo\\MapInfo\\Professional\\" + versions[i];

            // TODO: add operations only for existing versions of MapInfo. 
            // We need a way how to find an existing registry key. How to check the result of REG QUERY here?
            /*
                REG QUERY HKEY_CURRENT_USER\Software\MapInfo\MapInfo\Professional\1700\Tools64\99999
                IF %ERRORLEVEL% EQU 0 (
                   echo Found key
                ) ELSE (
                    echo Did not found key
                )
            */

            // TODO: add checks whether "99999" already exists in registry and pick another name if so.
            var reg_path = reg_ver_path + "\\Tools64\\99999"; 
            var plugin_path = "@TargetDir@\\share\\NextGIS\\MapInfo\\NextGISConnect";

            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Autoload", "/t", "REG_DWORD", "/d", "1");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Description", "/t", "REG_SZ", "/d", "NextGIS Connect for MapInfo");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "ImageUri", "/t", "REG_SZ", "/d", plugin_path + "\\nextgis.png");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Location", "/t", "REG_SZ", "/d", plugin_path + "\\NextGISConnect.mbx");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Owner", "/t", "REG_SZ", "/d", "MI_TOOLS");
            component.addElevatedOperation("Execute", "REG", "ADD", reg_path, "/v", "Title", "/t", "REG_SZ", "/d", "NextGIS Connect");
            
            // The following command is for deinstallation only:
            component.addElevatedOperation("Execute", "rem", "UNDOEXECUTE", "REG", "DELETE", reg_path, "/f");
        }
    }
}
