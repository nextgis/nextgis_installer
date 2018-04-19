/*******************************************************************************
**
** Project: NextGIS online/offline installer
** Author: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.com>
** Copyright (c) 2016 NextGIS <info@nextgis.com>
** License: GPL v.2
**
*******************************************************************************/

function Component()
{
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

    component.addOperation("Delete", "@HomeDir@/Library/LaunchAgents/setenv." + name + ".plist");
    component.addOperation("AppendFile", "@HomeDir@/Library/LaunchAgents/setenv." + name + ".plist", contentString);
    // Fix permissions
    component.addOperation("Execute", "{0,1,255}", "/bin/chmod", "644", "@HomeDir@/Library/LaunchAgents/setenv." + name + ".plist");
    component.addOperation("Execute", "{0,1,255}", "/bin/launchctl", "load", "-w", "@HomeDir@/Library/LaunchAgents/setenv." + name + ".plist");
    //, "UNDOEXECUTE", "{0,1,255}", "launchctl", "unload", "-w", "@HomeDir@/Library/LaunchAgents/setenv." + name + ".plist"
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") == "mac")
    {
        // Try to create directory
        component.addOperation( "Execute", "{0,1,255}", "/bin/mkdir", "@HomeDir@/Library/LaunchAgents" )

        component.addOperation( "NgFileEnvironmentVariable",
                                "PATH",
                                "@TargetDir@/usr/bin",
                                "@HomeDir@/.profile;@HomeDir@/.bash_profile" );
        component.addOperation( "NgFileEnvironmentVariable",
                                "PATH",
                                "$PATH",
                                "@HomeDir@/.profile;@HomeDir@/.bash_profile" );

        // Not work in GUI App - SetEnvMac("PATH", "@TargetDir@/usr/bin");
    }
}
