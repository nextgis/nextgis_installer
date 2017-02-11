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

Component.prototype.createOperations = function()
{
    component.createOperations();

    // fix paths in sipconfig.py
    component.addOperation( "LineReplace",
                            "@TargetDir@/Library/Python/2.7/site-packages/sipconfig.py",
                            "'default_mod_dir':",
                            "    'default_mod_dir':    '@TargetDir@/Library/Python/2.7/site-packages',"
                        );
    component.addOperation( "LineReplace",
                            "@TargetDir@/Library/Python/2.7/site-packages/sipconfig.py",
                            "'default_sip_dir':",
                            "    'default_sip_dir':    '@TargetDir@/usr/share/sip',"
                        );
    component.addOperation( "LineReplace",
                            "@TargetDir@/Library/Python/2.7/site-packages/sipconfig.py",
                            "'sip_config_args':",
                            "    'sip_config_args':    '--destdir @TargetDir@/usr --arch x86_64 --bindir @TargetDir@/usr/bin --incdir @TargetDir@/usr/include --sipdir @TargetDir@/usr/share/sip',"
                        );
    component.addOperation( "LineReplace",
                            "@TargetDir@/Library/Python/2.7/site-packages/sipconfig.py",
                            "'sip_inc_dir':",
                            "    'sip_inc_dir':    '@TargetDir@/usr/include',"
                        );
    component.addOperation( "LineReplace",
                            "@TargetDir@/Library/Python/2.7/site-packages/sipconfig.py",
                            "'sip_mod_dir':",
                            "    'sip_mod_dir':    '@TargetDir@/Library/Python/2.7/site-packages',"
                        );

    component.addOperation( "Mkdir", "@TargetDir@/usr/share/sip" );
    if (installer.value("os") == "win")
    {
        component.addOperation( "LineReplace",
                                "@TargetDir@/Library/Python/2.7/site-packages/sipconfig.py",
                                "'sip_bin':",
                                "    'sip_bin':    '@TargetDir@/usr/bin/sip.exe',"
                            );
    }
    else {
        component.addOperation( "LineReplace",
                                "@TargetDir@/Library/Python/2.7/site-packages/sipconfig.py",
                                "'sip_bin':",
                                "    'sip_bin':    '@TargetDir@/usr/bin/sip',"
                            );
    }
}
