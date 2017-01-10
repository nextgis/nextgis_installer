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

function CreateSymLink(name)
{
    component.addElevatedOperation("Execute", "{0}", "ln", "-s",
        "@TargetDir@/Applications/gdal.app/Contents/MacOS/" + name,
        "@TargetDir@/usr/bin/" + name);
    component.registerPathForUninstallation("@TargetDir@/usr/bin/" + name);
}

Component.prototype.createOperations = function()
{
    component.createOperations();

    if (installer.value("os") == "mac")
    {
        var utilities = [
            "gdalinfo",
            "gdaladdo",
            "gdalbuildvrt",
            "gdaldem",
            "gdalenhance",
            "gdallocationinfo",
            "gdalmanage",
            "gdalserver",
            "gdalsrsinfo",
            "gdaltindex",
            "gdaltransform",
            "gdalwarp",
            "gdal_contour",
            "gdal_grid",
            "gdal_rasterize",
            "gdal_translate",
            "nearblack",
            "testepsg",
            "ogr2ogr",
            "ogrtindex",
            "ogrinfo",
            "gnmmanage",
            "gnmanalyse"
        ];

        for ( i = 0; i < utilities.length; i++ ) {
            CreateSymLink(utilities[i]);
        }
    }
}
