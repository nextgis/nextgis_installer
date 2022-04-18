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

    if (installer.value("os") == "win")
    {
        // fix paths in sipconfig.py
        component.addOperation( "LineReplace",
                                "@TargetDir@/lib/Python36/site-packages/sipconfig.py",
                                "'default_mod_dir':",
                                "    'default_mod_dir':    '@TargetDir@/lib/Python36/site-packages',"
                            );
        component.addOperation( "LineReplace",
                                "@TargetDir@/lib/Python36/site-packages/sipconfig.py",
                                "'default_sip_dir':",
                                "    'default_sip_dir':    '@TargetDir@/share/sip',"
                            );
        component.addOperation( "LineReplace",
                                "@TargetDir@/lib/Python36/site-packages/sipconfig.py",
                                "'sip_config_args':",
                                "    'sip_config_args':    '--destdir @TargetDir@ --arch x86_64 --bindir @TargetDir@/bin --incdir @TargetDir@/include --sipdir @TargetDir@/share/sip',"
                            );
        component.addOperation( "LineReplace",
                                "@TargetDir@/lib/Python36/site-packages/sipconfig.py",
                                "'sip_inc_dir':",
                                "    'sip_inc_dir':    '@TargetDir@/include',"
                            );
        component.addOperation( "LineReplace",
                                "@TargetDir@/lib/Python36/site-packages/sipconfig.py",
                                "'sip_mod_dir':",
                                "    'sip_mod_dir':    '@TargetDir@/lib/Python36/site-packages',"
                            );

        component.addOperation( "Mkdir", "@TargetDir@/share/sip" );
        component.addOperation( "LineReplace",
                                "@TargetDir@/lib/Python36/site-packages/sipconfig.py",
                                "'sip_bin':",
                                "    'sip_bin':    '@TargetDir@/bin/sip.exe',"
                            );
    }
    else {
        // fix paths in sipconfig.py
        component.addOperation( "LineReplace",
                                "@TargetDir@/Library/Python/3.6/site-packages/sipconfig.py",
                                "'default_mod_dir':",
                                "    'default_mod_dir':    '@TargetDir@/Library/Python/3.6/site-packages',"
                            );
        component.addOperation( "LineReplace",
                                "@TargetDir@/Library/Python/3.6/site-packages/sipconfig.py",
                                "'default_sip_dir':",
                                "    'default_sip_dir':    '@TargetDir@/usr/share/sip',"
                            );
        component.addOperation( "LineReplace",
                                "@TargetDir@/Library/Python/3.6/site-packages/sipconfig.py",
                                "'sip_config_args':",
                                "    'sip_config_args':    '--destdir @TargetDir@/usr --arch x86_64 --bindir @TargetDir@/usr/bin --incdir @TargetDir@/usr/include --sipdir @TargetDir@/usr/share/sip',"
                            );
        component.addOperation( "LineReplace",
                                "@TargetDir@/Library/Python/3.6/site-packages/sipconfig.py",
                                "'sip_inc_dir':",
                                "    'sip_inc_dir':    '@TargetDir@/usr/include',"
                            );
        component.addOperation( "LineReplace",
                                "@TargetDir@/Library/Python/3.6/site-packages/sipconfig.py",
                                "'sip_mod_dir':",
                                "    'sip_mod_dir':    '@TargetDir@/Library/Python/3.6/site-packages',"
                            );

//        component.addOperation( "Mkdir", "@TargetDir@/usr/share/sip" );
        component.addOperation( "LineReplace",
                                "@TargetDir@/Library/Python/3.6/site-packages/sipconfig.py",
                                "'sip_bin':",
                                "    'sip_bin':    '@TargetDir@/usr/bin/sip',"
                            );
    }
}
