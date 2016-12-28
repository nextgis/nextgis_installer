function Component()
{

}


Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") == "mac")
    {
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdalinfo",
            "/usr/local/bin/gdalinfo");
        component.registerPathForUninstallation("/usr/local/bin/gdalinfo");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdaladdo",
            "/usr/local/bin/gdaladdo");
        component.registerPathForUninstallation("/usr/local/bin/gdaladdo");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdalbuildvrt",
            "/usr/local/bin/gdalbuildvrt");
        component.registerPathForUninstallation("/usr/local/bin/gdalbuildvrt");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdaldem",
            "/usr/local/bin/gdaldem");
        component.registerPathForUninstallation("/usr/local/bin/gdaldem");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdalenhance",
            "/usr/local/bin/gdalenhance");
        component.registerPathForUninstallation("/usr/local/bin/gdalenhance");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdallocationinfo",
            "/usr/local/bin/gdallocationinfo");
        component.registerPathForUninstallation("/usr/local/bin/gdallocationinfo");     
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdalmanage",
            "/usr/local/bin/gdalmanage");
        component.registerPathForUninstallation("/usr/local/bin/gdalmanage");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdalserver",
            "/usr/local/bin/gdalserver");
        component.registerPathForUninstallation("/usr/local/bin/gdalserver");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdalsrsinfo",
            "/usr/local/bin/gdalsrsinfo");
        component.registerPathForUninstallation("/usr/local/bin/gdalsrsinfo");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdaltindex",
            "/usr/local/bin/gdaltindex");
        component.registerPathForUninstallation("/usr/local/bin/gdaltindex");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdaltransform",
            "/usr/local/bin/gdaltransform");
        component.registerPathForUninstallation("/usr/local/bin/gdaltransform");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdalwarp",
            "/usr/local/bin/gdalwarp");
        component.registerPathForUninstallation("/usr/local/bin/gdalwarp");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdal_contour",
            "/usr/local/bin/gdal_contour");
        component.registerPathForUninstallation("/usr/local/bin/gdal_contour");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdal_grid",
            "/usr/local/bin/gdal_grid");
        component.registerPathForUninstallation("/usr/local/bin/gdal_grid");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdal_rasterize",
            "/usr/local/bin/gdal_rasterize");
        component.registerPathForUninstallation("/usr/local/bin/gdal_rasterize");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/gdal_translate",
            "/usr/local/bin/gdal_translate");
        component.registerPathForUninstallation("/usr/local/bin/gdal_translate");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/nearblack",
            "/usr/local/bin/nearblack");
        component.registerPathForUninstallation("/usr/local/bin/nearblack");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/testepsg",
            "/usr/local/bin/testepsg");
        component.registerPathForUninstallation("/usr/local/bin/testepsg");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/ogr2ogr",
            "/usr/local/bin/ogr2ogr");
        component.registerPathForUninstallation("/usr/local/bin/ogr2ogr");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/ogrlineref",
            "/usr/local/bin/ogrlineref");
        component.registerPathForUninstallation("/usr/local/bin/ogrlineref");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/ogrtindex",
            "/usr/local/bin/ogrtindex");
        component.registerPathForUninstallation("/usr/local/bin/ogrtindex");
        component.addElevatedOperation("Execute", "{0}", "ln", "-s",
            "@TargetDir@/Applications/gdal.app/Contents/MacOS/ogrinfo",
            "/usr/local/bin/ogrinfo");
        component.registerPathForUninstallation("/usr/local/bin/ogrinfo");
    }
}
