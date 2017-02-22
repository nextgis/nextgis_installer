/*******************************************************************************
**
** Project: NextGIS online/offline installer
** Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
** Copyright (c) 2017 NextGIS <info@nextgis.com>
** License: GPL v.2
**
*******************************************************************************/

function Component()
{

}

function CreateSymLink(name)
{
    component.addOperation("Execute", "{0}", "ln", "-s",
        "@TargetDir@/Applications/qca.app/Contents/MacOS/" + name,
        "@TargetDir@/usr/bin/" + name);
    component.registerPathForUninstallation("@TargetDir@/usr/bin/" + name);
}

function SetEnvMac(name, path)
{
    var contentString = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">
    <plist version=\"1.0\">\n        <dict>\n        <key>Label</key>\n        <string>setenv.";
    contentString += name;
    contentString += "</string>\n        <key>ProgramArguments</key>\n        <array>\n            <string>/bin/launchctl</string>\n            <string>setenv</string>\n            <string>";
    contentString += name;
    contentString += "</string>\n            <string>";
    contentString += path;
    contentString += "</string>\n        </array>\n        <key>RunAtLoad</key>\n        <true/>\n        <key>ServiceIPC</key>\n        <false/>\n    </dict>\n    </plist>";

    component.addOperation("AppendFile", "@HomeDir@/Library/LaunchAgents/setenv." + name + ".plist", contentString);
    component.addOperation("Execute", "{0}", "launchctl", "load", "-w", "@HomeDir@/Library/LaunchAgents/setenv." + name + ".plist",
                            "UNDOEXECUTE", "launchctl", "unload", "-w", "@HomeDir@/Library/LaunchAgents/setenv." + name + ".plist");                     
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") == "mac")
    {
        // Create qt.conf
        /* this should created by some utility package
        var settingsFile = "@TargetDir@/usr/bin/qt.conf";
        component.addOperation("Settings", "path="+settingsFile, "method=add_array_value",
            "key=Paths/Plugins", "value=@TargetDir@/Library/Plugins/Qt4/");
        component.addOperation("Settings", "path="+settingsFile, "method=add_array_value",
            "key=Paths/Translations", "value=@TargetDir@/Library/Translations/Qt4/");
        */

        component.addOperation( "AppendFile",
                                "@HomeDir@/.bash_profile",
                                "\nexport QCA_PLUGIN_PATH=@TargetDir@/Library/Plugins/Qt4/" );
        SetEnvMac("QCA_PLUGIN_PATH", "@TargetDir@/Library/Plugins/Qt4/");
    }
}
